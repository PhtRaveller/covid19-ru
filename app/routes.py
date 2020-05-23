"""Routes for CoVID-19 dashboard app."""

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

    # Check pre-rendered HTML
    rendered = data.get_rendered_page("country")

    if rendered:
        return rendered

    city = "Россия"

    main_links = filter_secondary_links(city)
    secondary_links = []

    # Getting data
    full_data = data.get_newest_data()
    country_data_full, country_data = data.get_region_data(full_data, city)
    swabs_data = data.get_swabs_data()
    swabs_data = swabs_data.join(country_data_full["total"], how="outer")

    # Cases statistics block
    stats = []

    for category in cts.CATEGORIES:
        style = cts.CATEGORIES_STYLES[category].copy()
        style["value"] = country_data[category]
        style["diff"] = country_data[f"{category}_diff"]
        stats.append(style)

    # Map plot
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
    map_plot = plotting.plot_map(map_data)

    # Cases plots
    cases_plot = plotting.plot_region(country_data_full, city)
    cases_log_plot = plotting.plot_region(country_data_full, city, log_y=True)

    # Swabs plots
    swabs_plot = plotting.plot_swabs(swabs_data, city)
    swabs_log_plot = plotting.plot_swabs(swabs_data, city, x_col="total")

    # Getting Bokeh components
    script, div = components({"cases": cases_plot, "cases_log": cases_log_plot,
                              "swabs": swabs_plot, "swabs_log": swabs_log_plot,
                              "map": map_plot, })

    # Rendering HTML
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

    # Check pre-rendered HTML
    city = "Москва"
    rendered = data.get_rendered_page(city)

    if rendered:
        return rendered

    main_links = [{"name": "Больницы", "link": "#hospitals"},
                  {"name": "Транспорт", "link": "#transport"}]
    secondary_links = filter_secondary_links(city)

    # Getting data
    full_data = data.get_newest_data()
    moscow_data_full, moscow_data = data.get_region_data(full_data, city)

    # Cases statistics block
    stats = []
    for category in cts.CATEGORIES[:-1]:
        style = cts.CATEGORIES_STYLES[category].copy()
        style["value"] = moscow_data[category]
        style["diff"] = moscow_data[f"{category}_diff"]
        stats.append(style)

    # Cases plots
    cases_plot = plotting.plot_region(moscow_data_full, city)
    cases_log_plot = plotting.plot_region(moscow_data_full, city, log_y=True)

    # Transport plots
    transport_data = data.get_data_by_key([cts.MSK_DIR, "transport"], sort_by="date", set_index="date")

    public_tr_plot = plotting.plot_region(transport_data / 100., city,
                                          plot_cols=[tr["key"] for tr in cts.PUBLIC_TR_COLS],
                                          legend_map=[tr["name"] for tr in cts.PUBLIC_TR_COLS],
                                          legend_loc="top_right",
                                          dt_fmt="%d-%m-%Y %H:%S",
                                          fmt="{0 %}",
                                          set_yticks=True,
                                          width_policy="max",
                                          height=int(0.75*cfg.MAX_MAIN_HEIGHT),
                                          xaxis_ticks=5, yrange=(-1.1, 0))
    private_tr_plot = plotting.plot_region(transport_data / 100., city,
                                           plot_cols=[tr["key"] for tr in cts.PRIVATE_TR_COLS],
                                           legend_map=[tr["name"] for tr in cts.PRIVATE_TR_COLS],
                                           legend_loc="top_right",
                                           dt_fmt="%d-%m-%Y %H:%S",
                                           fmt="{0 %}",
                                           set_yticks=True,
                                           width_policy="max",
                                           height=int(0.75*cfg.MAX_MAIN_HEIGHT),
                                           xaxis_ticks=5, yrange=(-1.1, 0))
    plots = {"cases": cases_plot, "cases_log": cases_log_plot,
             "public_transport": public_tr_plot, "private_transport": private_tr_plot}

    # Transport block
    transport_data_latest = transport_data.iloc[-1].to_dict()
    tr_stats = []

    for category in cts.PUBLIC_TR_COLS + cts.PRIVATE_TR_COLS:
        tr_stats.append({"name": category["name"].capitalize(),
                         "value": transport_data_latest[category["key"]]})

    # Age distribution
    age_data = data.get_data_by_key([cts.MSK_DIR, "age"], sort_by="date", set_index="date")
    raw_ages_cols = age_data.columns[1:-4:2].tolist()
    raw_perc_cols = age_data.columns[2:-4:2].tolist()
    raw_ages_cols = ["children"] + raw_ages_cols
    raw_perc_cols = ["children%"] + raw_perc_cols

    daily_stats = moscow_data_full[cts.DAILY_DISCHARGE_CATEGORIES].diff().loc[age_data.index]

    daily_plot = plotting.plot_cases_bar(age_data[raw_ages_cols], city,
                                         cases_neg=daily_stats, yrange=cts.DAILY_RANGE,
                                         width=cfg.MAX_MAIN_WIDTH * 2,
                                         legend_loc="bottom_left")
    for cl in raw_perc_cols:
        age_data[f"{cl}_perc"] = age_data[cl] / 100.

    age_plot = plotting.plot_cases_bar(age_data.rename({"total": "total_cases"}, axis=1),
                                       city, pos_cols=raw_perc_cols,
                                       width=cfg.MAX_MAIN_WIDTH * 2, height=cfg.MIN_MAIN_HEIGHT,
                                       skip_legend=True,
                                       total_col="total_cases",
                                       fmt="{0.0 %}",
                                       suffix="_perc")
    plots["daily_plot"] = daily_plot
    plots["age_plot"] = age_plot

    # Hospitals
    hospitals = []
    for hospital in cts.MSK_HOSPITALS:
        hospital_data = data.get_data_by_key([cts.MSK_DIR, cts.MSK_HOSPITALS_DIR, hospital["key"]])
        hospital_plot = plotting.plot_region(hospital_data, hospital["name"],
                                             plot_cols=[tr["key"] for tr in hospital["fields"]],
                                             legend_map=[tr["name"] for tr in hospital["fields"]],
                                             glyphs={tr["key"]: tr["glyph"]
                                                     for tr in hospital["fields"] if "glyph" in tr},
                                             alphas={tr["key"]: tr["alpha"]
                                                     for tr in hospital["fields"] if "alpha" in tr},
                                             bar_bottom=0,
                                             alpha=0.9,
                                             legend_loc="top_left",
                                             width_policy="max",
                                             width=cfg.MAX_MAIN_WIDTH * 2,
                                             height_policy="fit",
                                             additional_tools=["ywheel_zoom", "ypan", "reset"])
        plots[hospital["key"]] = hospital_plot
        hospitals.append(hospital)

    # Getting Bokeh components
    script, div = components(plots)

    for hospital in hospitals:
        hospital_plot = div.pop(hospital["key"])
        hospital["plot"] = hospital_plot

    # Rendering HTML
    rendered = render_template("moscow.html", city=city,
                               main_links=main_links,
                               secondary_links=secondary_links,
                               stats=stats,
                               tr_stats=tr_stats,
                               bokeh_script=script,
                               hospitals=hospitals,
                               **div)
    data.save_rendered_page("moscow", rendered)

    return rendered
