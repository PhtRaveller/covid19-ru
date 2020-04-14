"""Routes for CoVID-19 dashboard app."""

from datetime import datetime
from flask import render_template
from app import covid_app
from app import data
from app import plotting
from app import config as cfg
from app import constants as cts
from bokeh.embed import components

data_cache = {}


def invalid_cache(cache, key, time):
    """Check if cache entry is still valid."""
    return cache.get(key, None) is None or time - cache[key]["time"] > cfg.CACHE_AGE


@covid_app.route("/")
def index():
    """Main page of the dashboard."""

    now = datetime.utcnow()
    main_links = []
    secondary_links = cts.REGIONAL_LINKS[:2]

    if invalid_cache(data_cache, "stats_data", now):
        if invalid_cache(data_cache, "full_data", now):
            data_cache["full_data"] = {"time": now, "value": data.get_newest_data()}

        country_data = data_cache["full_data"]["value"]["Россия"]
        country_data["swabs"] = country_data["swabs"] / 1000
        country_data = (country_data
                        .join(country_data.diff().rename(lambda cl: f"{cl}_diff", axis=1))
                        .iloc[-1]
                        .to_dict())
        data_cache["stats_data"] = {"time": now, "value": country_data}

    country_data = data_cache["stats_data"]["value"]

    stats = []
    for category in cts.CATEGORIES:
        style = cts.CATEGORIES_STYLES[category].copy()
        style["value"] = country_data[category]
        style["diff"] = country_data[f"{category}_diff"]
        stats.append(style)

    city = "Россия"

    if invalid_cache(data_cache, "map_data", now):
        borders = data.get_geo_data()
        latest_data = data_cache["full_data"]["value"].iloc[-1].unstack(level=-1)
        latest_diff = (data_cache["full_data"]["value"]
                       .diff()
                       .iloc[-1]
                       .unstack(level=-1)
                       .rename(lambda x: f"{x}_diff", axis=1))
        map_data = (borders
                    .join(latest_data, on="REGION")
                    .join(latest_diff, on="REGION")
                    .fillna(0))
        map_data["total_color"] = 1. + map_data["total"]
        data_cache["map_data"] = {"time": now, "value": map_data}

    cases_plot = plotting.plot_region(data_cache["full_data"]["value"]["Россия"])
    swabs_plot = plotting.plot_region(data_cache["full_data"]["value"]["Россия"],
                                      plot_cols=["swabs"], legend_map=["тыс. тестов проведено"], bar=True)
    swabs_log_plot = plotting.plot_region(data_cache["full_data"]["value"]["Россия"], log_y=True,
                                          plot_cols=["swabs"], legend_map=["тыс. тестов проведено"], bar=True)
    cases_log_plot = plotting.plot_region(data_cache["full_data"]["value"]["Россия"], log_y=True)
    map_plot = plotting.plot_map(data_cache["map_data"]["value"])

    script, div = components({"cases": cases_plot, "map": map_plot, "cases_log": cases_log_plot,
                              "swabs": swabs_plot, "swabs_log": swabs_log_plot})
    return render_template("main.html", city=city,
                           main_links=main_links, secondary_links=secondary_links,
                           stats=stats,
                           bokeh_script=script,
                           **div)
