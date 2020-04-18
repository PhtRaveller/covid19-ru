"""Routes for CoVID-19 dashboard app."""

from datetime import datetime
from flask import render_template
from app import covid_app
from app import data
from app import plotting
from app import config as cfg
from app import constants as cts
from bokeh.embed import components


def filter_secondary_links(region, num_links=2):
    """Return `num_links` secondary links, except `region`."""

    return [link for link in cts.REGIONAL_LINKS if link["name"] != region][:num_links]


@covid_app.route("/")
def index():
    """Main page of the dashboard."""

    rendered = data.get_rendered_page("country")

    if rendered:
        return rendered

    city = "Россия"

    main_links = []
    secondary_links = filter_secondary_links(city)

    full_data = data.get_newest_data()
    country_data_full, country_data = data.get_region_data(full_data, city)

    stats = []

    for category in cts.CATEGORIES:
        style = cts.CATEGORIES_STYLES[category].copy()
        style["value"] = country_data[category]
        style["diff"] = country_data[f"{category}_diff"]
        stats.append(style)

    borders = data.get_geo_data()
    latest_data = full_data.iloc[-1].unstack(level=-1)
    latest_diff = (full_data
                   .diff()
                   .iloc[-1]
                   .unstack(level=-1)
                   .rename(lambda x: f"{x}_diff", axis=1))
    map_data = (borders
                .join(latest_data, on="REGION")
                .join(latest_diff, on="REGION")
                .fillna(0))

    map_data["total_color"] = 1. + map_data["total"]

    # Cases plots
    cases_plot = plotting.plot_region(country_data_full, city)
    cases_log_plot = plotting.plot_region(country_data_full, city, log_y=True)

    # Swabs plots
    swabs_plot = plotting.plot_region(country_data_full, city,
                                      plot_cols=["swabs"],
                                      legend_map=["тыс. тестов проведено"],
                                      bar=True)
    swabs_log_plot = plotting.plot_region(country_data_full, city, log_y=True,
                                          plot_cols=["swabs"],
                                          legend_map=["тыс. тестов проведено"],
                                          bar=True)

    # Map plot
    map_plot = plotting.plot_map(map_data)

    # Getting Bokeh components
    script, div = components({"cases": cases_plot, "cases_log": cases_log_plot,
                              "swabs": swabs_plot, "swabs_log": swabs_log_plot,
                              "map": map_plot, })

    rendered = render_template("main.html", city=city,
                               main_links=main_links,
                               secondary_links=secondary_links,
                               stats=stats,
                               bokeh_script=script,
                               **div)
    data.save_rendered_page("country", rendered)
    return rendered


@covid_app.route("/moscow")
def moscow():
    """Moscow-specific page."""

    city = "Москва"

    main_links = [{"name": "Больницы", "link": "#hospitals"},
                  {"name": "Транспорт", "link": "#transport"}]
    secondary_links = filter_secondary_links(city)

    full_data = data.get_newest_data()
    moscow_data_full, moscow_data = data.get_region_data(full_data, city)

    stats = []
    for category in cts.CATEGORIES[:-1]:
        style = cts.CATEGORIES_STYLES[category].copy()
        style["value"] = moscow_data[category]
        style["diff"] = moscow_data[f"{category}_diff"]
        stats.append(style)

    # Cases plots
    cases_plot = plotting.plot_region(moscow_data_full, city)
    cases_log_plot = plotting.plot_region(moscow_data_full, city, log_y=True)

    script, div = components({"cases": cases_plot, "cases_log": cases_log_plot})

    return render_template("moscow.html", city=city,
                           main_links=main_links,
                           secondary_links=secondary_links,
                           stats=stats,
                           bokeh_script=script,
                           **div)
