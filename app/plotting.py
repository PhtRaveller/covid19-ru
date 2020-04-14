from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import GeoJSONDataSource
from bokeh.models import DatetimeTickFormatter, PrintfTickFormatter
from bokeh.models import LogColorMapper, HoverTool, WheelZoomTool
from app import config as cfg
from app import constants as cts


CASES_TOOLTIP = """<div class="plot-tooltip">
    <h4>Россия</h4>
    <div>
        <span style="font-weight: bold;">Дата: </span>@date_str
    </div>"""
CASES_TOOLTIP_FOOTER = """<div>
        <span style="font-weight: bold;">{value_type}: </span>@{col}{{0,0}}
    </div>
</div>
"""
MAP_TOOLTIP = """
<div class="plot-tooltip">
    <div class="mb-2">
        <h4>@REGION</h4>
    </div>
    <div>
        <span style="font-weight: bold;">Выявлено: </span>@total{0,0}<sup>@total_diff{+0,0}</sup>
    </div>
    <div>
        <span style="font-weight: bold;">Выздоровело: </span>@recovered{0,0}<sup>@recovered_diff{+0,0}</sup>
    </div>
    <div>
        <span style="font-weight: bold;">Умерло: </span>@died{0,0}<sup>@died_diff{+0,0}</sup>
    </div>
</div>
"""


def plot_region(ds, log_y=False, plot_cols=cts.CATEGORIES[:3],
                legend_map=cts.LEGEND_MAP, color_ramp=cts.COLOR_RAMP,
                alpha=0.7, line_width=2, ms=8, bar=False, bar_width=cfg.DATE_WIDTH,
                height=cfg.MAX_MAIN_HEIGHT, width=cfg.MAX_MAIN_WIDTH):
    """Make a single region plot."""

    tools = "save"
    ds = ds.reset_index()
    ds["date_str"] = ds.date.dt.strftime("%d-%m-%Y")

    if log_y:
        p = figure(x_axis_type="datetime", y_axis_type="log", tools=tools,
                   height_policy="fit", plot_height=height, max_height=height,
                   plot_width=width, max_width=width, width_policy="fixed")
        p.yaxis[0].formatter = PrintfTickFormatter(format="%7.0f")
    else:
        p = figure(x_axis_type="datetime", tools=tools,
                   height_policy="fit", plot_height=height, max_height=height,
                   plot_width=width, max_width=width, width_policy="fixed")
    p.toolbar.logo = None

    for ci, cl in enumerate(plot_cols):
        current_data = ds[ds[cl].notnull()].copy()
        if bar:
            cr = p.vbar(x="date", top=cl, width=bar_width, bottom=100,
                        color=color_ramp[ci % len(color_ramp)],
                        source=current_data,
                        alpha=alpha, legend_label=legend_map[ci])
        else:
            p.line(x="date", y=cl, color=color_ramp[ci % len(color_ramp)],
                   source=current_data,
                   alpha=alpha, line_width=line_width)
            cr = p.circle(x="date",  y=cl, color=color_ramp[ci % len(color_ramp)],
                          source=current_data,
                          alpha=alpha, size=ms, fill_color="white",
                          legend_label=legend_map[ci])

        local_tooltip = CASES_TOOLTIP_FOOTER.format(value_type=legend_map[ci].capitalize(),
                                                    col=cl)
        p.add_tools(HoverTool(renderers=[cr],
                              tooltips=CASES_TOOLTIP + local_tooltip,
                              formatters={"date": "datetime"},
                              toggleable=False))

    p.xaxis[0].formatter = DatetimeTickFormatter(days=['%d %b'])

    p.legend.location = "top_left"

    doc = curdoc()
    doc.theme = cfg.THEME
    return p


def plot_map(ds, palette=cts.MAP_PALLETE, breeze=cfg.MAP_BREEZE):
    """Plot cases map."""

    minx, miny, maxx, maxy = ds.total_bounds
    x_range = maxx - minx
    y_range = maxy - miny
    ar = (maxx - minx) / (maxy - miny)
    x_range = (minx - breeze * x_range, maxx + breeze * x_range)
    y_range = (miny - breeze * y_range, maxy + breeze * y_range)

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

    p.add_tools(HoverTool(tooltips=MAP_TOOLTIP,
                          point_policy="follow_mouse",
                          toggleable=False))
    wheel_zoom = WheelZoomTool(zoom_on_axis=False)
    p.add_tools(wheel_zoom)
    p.toolbar.active_scroll = wheel_zoom

    doc = curdoc()
    doc.theme = cfg.THEME
    return p
