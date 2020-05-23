from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import GeoJSONDataSource
from bokeh.models import DatetimeTickFormatter, PrintfTickFormatter, NumeralTickFormatter
from bokeh.models import HoverTool, WheelZoomTool
from bokeh.models import LogColorMapper
from bokeh.models import Label
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

    # Setting tools
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
                   active_drag=None,
                   active_scroll=active_scroll)
        p.yaxis[0].formatter = PrintfTickFormatter(format="%7.0f")
    else:
        p = figure(x_axis_type="datetime", tools=tools,
                   plot_height=height, max_height=height, min_height=height,
                   height_policy=height_policy,
                   plot_width=width, max_width=width,
                   width_policy=width_policy,
                   active_drag=None,
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
    else:
        p.yaxis[0].formatter = NumeralTickFormatter(format="0a")

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


def plot_swabs(ds, city, start_date=cts.SWABS_START_DATE, dt_col="date",
               plot_cols=cts.SWABS_CATEGORIES, legend_map=cts.SWABS_LEGEND_MAP,
               x_col="date",
               range_padding=0.075,
               y_range=cts.SWABS_RANGE,
               alpha_factor=cts.SWABS_ALPHA,
               size_factor=cts.SWABS_SIZE,
               delay_factor=cts.SWABS_DELAY,
               log_y=False, dt_fmt="%d-%m-%Y", fmt="{0,0}", set_yticks=False,
               color_ramp=cts.COLOR_RAMP, alpha=0.7,
               line_width=2, ms=8,
               glyphs={}, alphas={},
               height=cfg.MAX_MAIN_HEIGHT, height_policy="fit",
               width=cfg.MAX_MAIN_WIDTH, width_policy="fixed",
               legend_loc="top_left", xaxis_ticks=None, yrange=None):
    """Custom plot for swabs."""

    tools = "save"

    # Preparing data
    ds = ds.loc[start_date:].reset_index()
    ds["date_str"] = ds[dt_col].dt.strftime(dt_fmt)
    x_range_raw = (ds[x_col].min(), ds[x_col].max())

    if y_range is None:
        y_range_raw = (ds["swabs_clean"].min(), ds["swabs_clean"].max())
    else:
        y_range_raw = y_range

    if range_padding is not None:
        x_range_width = x_range_raw[1] - x_range_raw[0]
        y_range_width = y_range_raw[1] - y_range_raw[0]
        x_range = (x_range_raw[0] - range_padding * x_range_width, x_range_raw[1] + range_padding * x_range_width)
        y_range = (y_range_raw[0] - range_padding * y_range_width, y_range_raw[1] + range_padding * y_range_width)
    else:
        x_range = x_range_raw
        y_range = y_range_raw

    # Creating figures
    if log_y:
        if x_col == dt_col:
            p = figure(x_axis_type="datetime", x_range=x_range, y_range=y_range, y_axis_type="log", tools=tools)
            p.xaxis[0].formatter = DatetimeTickFormatter(days=['%d %b'])
        else:
            p = figure(x_range=x_range, y_range=y_range, y_axis_type="log", tools=tools)
            p.xaxis[0].formatter = NumeralTickFormatter(format="0a")
    else:
        if x_col == dt_col:
            p = figure(x_axis_type="datetime", x_range=x_range, y_range=y_range, tools=tools)
            p.xaxis[0].formatter = DatetimeTickFormatter(days=['%d %b'])
        else:
            p = figure(x_range=x_range, y_range=y_range, tools=tools)
            p.xaxis[0].formatter = NumeralTickFormatter(format="0a")

    p.toolbar.logo = None
    p.plot_height = height
    p.max_height = height
    p.min_height = height
    p.height_policy = height_policy
    p.plot_width = width
    p.max_width = width
    p.width_policy = width_policy
    p.yaxis[0].formatter = NumeralTickFormatter(format="0a")

    ds["alpha"] = (ds["total"].shift(delay_factor) / ds["swabs_clean"]) * alpha_factor
    ds["size"] = ds["swabs_derived_daily"] / size_factor
    ds["positive"] = ds["total"].shift(delay_factor) / ds["swabs_clean"]

    cr = p.circle(x=x_col, y="swabs_clean", size="size",
                  source=ds[ds["swabs_clean"].notnull()],
                  color="#990800", alpha="alpha",
                  line_color="white")

    p.yaxis[0].formatter = NumeralTickFormatter(format="0a")
    p.add_tools(HoverTool(renderers=[cr],
                          tooltips=cts.SWABS_TOOLTIP,
                          formatters={'date': 'datetime'},
                          toggleable=False))

    p.toolbar.logo = None

    # Setting axis labels
    if x_col != dt_col:
        x_label = Label(x=x_range_raw[1], y=y_range_raw[0], text="выявлено", render_mode='css',
                        text_font_size="10pt", text_align="right", text_baseline="middle")
        y_label = Label(x=x_range_raw[0], y=y_range_raw[1], text="тестов всего", render_mode='css',
                        text_baseline="top", text_font_size="10pt")
        p.add_layout(x_label)
        p.add_layout(y_label)

    # Setting X-ticker
    if xaxis_ticks is not None:
        p.xaxis[0].ticker.desired_num_ticks = xaxis_ticks

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


def plot_cases_bar(cases_pos, city, cases_neg=None,
                   pos_cols=None, neg_cols=None, 
                   dt_col="date", fillna=0,
                   dt_fmt="%d-%m-%Y", fmt="{0,0}",
                   pos_legend_map=cts.DAILY_LEGEND_MAP,
                   neg_legend_map=cts.DAILY_LEGEND_MAP,
                   pos_color_ramp=cts.AGES_COLOR_RAMP,
                   neg_color_ramp=cts.DISCHARGES_COLOR_RAMP,
                   alpha=0.7, line_width=2, line_color="white",
                   hatch_pattern="x", hatch_color="white",
                   suffix="",
                   bar_width=cts.DAILY_WIDTH,
                   total_col="total",
                   height=cfg.MAX_MAIN_HEIGHT, height_policy="fit",
                   width=cfg.MAX_MAIN_WIDTH, width_policy="fixed",
                   additional_tools=[], legend_loc="top_left",
                   xaxis_ticks=None, yrange=None, set_yticks=False, skip_legend=False):
    """Make a (stacked) bar plot for a region."""

    # We create the stacked bar manually for more flexibility in tooltips
    # Prepare positive part
    if cases_pos is not None:
        cases_pos = cases_pos.copy()

        # Fixing possible naming issues for Bokeh
        cases_pos = cases_pos.rename(lambda cl: cl.replace("+", ""), axis=1)
        cases_pos = cases_pos.rename(lambda cl: cl.replace("%", "_"), axis=1)
        cases_pos = cases_pos.rename(lambda cl: cl.replace(" ", "_"), axis=1)
        cases_pos = cases_pos.rename(lambda cl: cl.replace("-", "_"), axis=1)
        pos_legend_map = {k.replace(" ", "_").replace("%", "_").replace("-", "_").replace("+", ""): v
                          for k, v in pos_legend_map.items()}

        pos_cols = cases_pos.columns.tolist() if pos_cols is None else pos_cols
        pos_cols = [cl.replace(" ", "_").replace("%", "_").replace("-", "_").replace("+", "")
                    for cl in pos_cols]
        cases_pos = cases_pos.reset_index()

        if fillna is not None:
            cases_pos.fillna(0, inplace=True)

        for ci, cl in enumerate(pos_cols[1:]):
            cases_pos[f"{cl}_bottom"] = cases_pos[pos_cols[:(ci+1)]].sum(axis=1)

        for ci, cl in enumerate(pos_cols[1:]):
            cases_pos[f"{cl}_top"] = cases_pos[cl] + cases_pos[f"{cl}_bottom"]

        cases_pos[f"{pos_cols[0]}_bottom"] = 0
        cases_pos[f"{pos_cols[0]}_top"] = cases_pos[pos_cols[0]]

        cases_pos["date_str"] = cases_pos[dt_col].dt.strftime(dt_fmt)
        cases_pos["total"] = cases_pos[pos_cols].sum(axis=1)

    # Prepare positive part
    if cases_neg is not None:
        cases_neg = cases_neg.copy()

        # Fixing possible naming issues for Bokeh
        cases_neg = cases_neg.rename(lambda cl: cl.replace("+", ""), axis=1)
        cases_neg = cases_neg.rename(lambda cl: cl.replace("%", "_"), axis=1)
        cases_neg = cases_neg.rename(lambda cl: cl.replace(" ", "_"), axis=1)
        cases_neg = cases_neg.rename(lambda cl: cl.replace("-", "_"), axis=1)
        neg_legend_map = {k.replace(" ", "_").replace("%", "_").replace("-", "_").replace("+", ""): v
                          for k, v in neg_legend_map.items()}

        neg_cols = cases_neg.columns.tolist() if neg_cols is None else neg_cols
        neg_cols = [cl.replace(" ", "_").replace("%", "_").replace("-", "_").replace("+", "")
                    for cl in neg_cols]
        cases_neg = cases_neg.reset_index()
        if fillna is not None:
            cases_neg.fillna(0, inplace=True)

        cases_neg["total"] = cases_neg.sum(axis=1)

        for ci, cl in enumerate(neg_cols[1:]):
            cases_neg[f"{cl}_bottom"] = cases_neg[neg_cols[:(ci+1)]].sum(axis=1) - cases_neg["total"]

        for ci, cl in enumerate(neg_cols[1:]):
            cases_neg[f"{cl}_top"] = cases_neg[cl] + cases_neg[f"{cl}_bottom"]

        cases_neg[f"{neg_cols[0]}_bottom"] = - cases_neg["total"]
        cases_neg[f"{neg_cols[0]}_top"] = cases_neg[neg_cols[0]] - cases_neg["total"]

        cases_neg["date_str"] = cases_neg[dt_col].dt.strftime(dt_fmt)

    tools = ["save"]

    p = figure(x_axis_type="datetime", tools=tools,
               plot_height=height, max_height=height, min_height=height,
               height_policy=height_policy,
               plot_width=width, max_width=width,
               width_policy=width_policy,
               active_drag=None)
    p.toolbar.logo = None

    if cases_pos is not None:
        for ci, cl in enumerate(pos_cols):
            bar_params = dict(color=pos_color_ramp[ci], width=bar_width,
                              alpha=alpha, line_color=line_color)

            if not skip_legend:
                bar_params["legend_label"] = pos_legend_map[cl]

            vb = p.vbar(x=dt_col, bottom=f"{cl}_bottom", top=f"{cl}_top", source=cases_pos, **bar_params)
            tooltip_header = cts.CASES_TOOLTIP.format(city=city)
            tooltip_footer = cts.DAILY_TOOLTIP_FOOTER.format(value_type=data.capitalize(pos_legend_map[cl]),
                                                             col=f"{cl}{suffix}",
                                                             fmt=fmt,
                                                             total_col=total_col)
            hover = HoverTool(tooltips=tooltip_header + tooltip_footer, renderers=[vb],
                              toggleable=False)
            p.add_tools(hover)

    if cases_neg is not None:
        for ci, cl in enumerate(neg_cols):
            bar_params = dict(color=neg_color_ramp[ci], width=bar_width,
                              alpha=alpha, line_color=line_color,
                              hatch_pattern=hatch_pattern, hatch_color=hatch_color)

            if not skip_legend:
                bar_params["legend_label"] = neg_legend_map[cl]

            vb = p.vbar(x=dt_col, bottom=f"{cl}_bottom", top=f"{cl}_top", source=cases_neg, **bar_params)
            tooltip_header = cts.CASES_TOOLTIP.format(city=city)
            tooltip_footer = cts.DISCHARGES_TOOLTIP_FOOTER.format(value_type=data.capitalize(neg_legend_map[cl]),
                                                                  col=f"{cl}{suffix}",
                                                                  fmt=fmt,
                                                                  total_col=total_col)
            hover = HoverTool(tooltips=tooltip_header + tooltip_footer, renderers=[vb],
                              toggleable=False)
            p.add_tools(hover)

    # Setting ticks
    p.xaxis[0].formatter = DatetimeTickFormatter(days=['%d %b'])

    if set_yticks:
        p.yaxis[0].formatter = NumeralTickFormatter(format="0 %")
    else:
        p.yaxis[0].formatter = NumeralTickFormatter(format="0a")

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
