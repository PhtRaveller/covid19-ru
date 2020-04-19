from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import GeoJSONDataSource
from bokeh.models import DatetimeTickFormatter, PrintfTickFormatter, NumeralTickFormatter
from bokeh.models import HoverTool, WheelZoomTool
from bokeh.models import LogColorMapper
from app import config as cfg
from app import constants as cts
from app import data


def plot_region(ds, city,
                plot_cols=cts.CATEGORIES[:3], dt_col="date", legend_map=cts.LEGEND_MAP,
                log_y=False, dt_fmt="%d-%m-%Y", fmt="{0,0}", set_yticks=False,
                color_ramp=cts.COLOR_RAMP, alpha=0.7,
                line_width=2, ms=8,
                bar=False, bar_width=cfg.DATE_WIDTH, bar_bottom=100,
                glyphs={}, alphas={},
                height=cfg.MAX_MAIN_HEIGHT, height_policy="fit",
                width=cfg.MAX_MAIN_WIDTH, width_policy="fixed",
                additional_tools=[], legend_loc="top_left",
                xaxis_ticks=None, yrange=None):
    """Make a single region plot."""

    # Setiing tools
    active_zooms = [tool for tool in additional_tools if "zoom" in tool]

    if len(active_zooms) != 0:
        active_scroll = active_zooms[0]
    else:
        active_scroll = "auto"

    tools = ",".join(["save"] + additional_tools)

    # Preparing data
    ds = ds.reset_index()
    ds["date_str"] = ds.date.dt.strftime(dt_fmt)

    # Fix any keys with spaces
    ds = ds.rename(lambda cl: cl.replace(" ", "_"), axis=1)
    plot_cols = [cl.replace(" ", "_") for cl in plot_cols]
    glyphs = {cl.replace(" ", "_"): glyph for cl, glyph in glyphs.items()}
    alphas = {cl.replace(" ", "_"): a for cl, a in alphas.items()}

    # Creating figures
    if log_y:
        p = figure(x_axis_type="datetime", y_axis_type="log", tools=tools,
                   plot_height=height, max_height=height, min_height=height,
                   height_policy=height_policy,
                   plot_width=width, max_width=width,
                   width_policy=width_policy,
                   active_scroll=active_scroll)
        p.yaxis[0].formatter = PrintfTickFormatter(format="%7.0f")
    else:
        p = figure(x_axis_type="datetime", tools=tools,
                   plot_height=height, max_height=height, min_height=height,
                   height_policy=height_policy,
                   plot_width=width, max_width=width,
                   width_policy=width_policy,
                   active_scroll=active_scroll)
    p.toolbar.logo = None

    # Plot each column
    for ci, cl in enumerate(plot_cols):
        current_data = ds[ds[cl].notnull()].copy()  # remove any NaNs

        if bar or glyphs.get(cl, None) == "bar":
            cr = p.vbar(x=dt_col, top=cl, width=bar_width, bottom=bar_bottom,
                        color=color_ramp[ci % len(color_ramp)],
                        source=current_data,
                        alpha=alphas.get(cl, alpha),
                        legend_label=legend_map[ci],
                        line_width=0)
        else:
            p.line(x=dt_col, y=cl,
                   color=color_ramp[ci % len(color_ramp)],
                   source=current_data,
                   alpha=alpha,
                   line_width=line_width)

            cr = p.circle(x=dt_col,  y=cl,
                          color=color_ramp[ci % len(color_ramp)],
                          source=current_data,
                          alpha=alpha, size=ms, fill_color="white",
                          legend_label=legend_map[ci])

        # Formatting tooltips
        tooltip_header = cts.CASES_TOOLTIP.format(city=city)
        tooltip_footer = cts.CASES_TOOLTIP_FOOTER.format(value_type=data.capitalize(legend_map[ci]),
                                                         col=cl, fmt=fmt)
        # Adding series specific hover
        p.add_tools(HoverTool(renderers=[cr],
                              tooltips=tooltip_header + tooltip_footer,
                              formatters={dt_col: "datetime"},
                              toggleable=False))

    # Setting ticks
    p.xaxis[0].formatter = DatetimeTickFormatter(days=['%d %b'])

    if set_yticks:
        p.yaxis[0].formatter = NumeralTickFormatter(format="0 %")

    # Setting legend
    p.legend.location = legend_loc
    p.legend.background_fill_alpha = 0.4

    # Setting X-ticker
    if xaxis_ticks is not None:
        p.xaxis[0].ticker.desired_num_ticks = xaxis_ticks

    # Setting Y-axis range
    if yrange is not None:
        p.y_range.start = yrange[0]
        p.y_range.end = yrange[1]

    # Applying theme
    doc = curdoc()
    doc.theme = cfg.THEME
    return p


def plot_map(ds, palette=cts.MAP_PALLETE, breeze=cfg.MAP_BREEZE):
    """Plot cases map."""

    # Calculating map bounds
    minx, miny, maxx, maxy = ds.total_bounds
    x_range = maxx - minx
    y_range = maxy - miny
    ar = (maxx - minx) / (maxy - miny)
    x_range = (minx - breeze * x_range, maxx + breeze * x_range)
    y_range = (miny - breeze * y_range, maxy + breeze * y_range)

    # Preparing data
    ds = GeoJSONDataSource(geojson=ds.to_json())
    tools = "pan,reset,save"
    color_mapper = LogColorMapper(palette=tuple(reversed(palette)))

    p = figure(tools=tools, x_range=x_range, y_range=y_range, aspect_ratio=ar,
               x_axis_location=None, y_axis_location=None, match_aspect=True)

    p.grid.grid_line_color = None
    p.toolbar.logo = None

    p.patches('xs', 'ys', fill_alpha=0.7,
              fill_color={'field': 'total_color', 'transform': color_mapper},
              line_color='gray', line_width=0.25, source=ds)

    p.add_tools(HoverTool(tooltips=cts.MAP_TOOLTIP,
                          point_policy="follow_mouse",
                          toggleable=False))
    # Adding zoom tool
    wheel_zoom = WheelZoomTool(zoom_on_axis=False)
    p.add_tools(wheel_zoom)
    p.toolbar.active_scroll = wheel_zoom

    # Applying theme
    doc = curdoc()
    doc.theme = cfg.THEME
    return p
