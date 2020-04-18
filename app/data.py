"""Various data utilities."""

import os
import pathlib
import pandas as pd
import geopandas as gpd
from app import config as cfg


def get_geo_data():
    """Read administrative borders."""

    root_dir = pathlib.Path(__file__).parent.parent
    geodata = gpd.read_file(root_dir.joinpath(cfg.GEODATA))
    return geodata


def get_newest_data():
    """
    Calculate the most recent data for all regions.

    Return a dataframe indexed and sorted by date with column MultiIndex (region, category).

    To get a single region, do `df[region]` on return value.

    """

    root_dir = pathlib.Path(__file__).parent.parent
    data = pd.read_csv(root_dir.joinpath(cfg.CSVDATA))
    data["date"] = pd.to_datetime(data["date"], dayfirst=True)
    data = data.set_index(["date", "category"]).unstack(level=-1)
    return data.sort_index()


def get_region_data(df, region):
    """Get data. along with diffs for `region`."""

    # Get data for this region
    country_data = df[region]

    # Normalize swabs
    country_data["swabs"] = country_data["swabs"] / 1000

    country_data = (country_data
                    .join(country_data
                          .diff()
                          .rename(lambda cl: f"{cl}_diff", axis=1)))
    return country_data, country_data.iloc[-1].to_dict()


def get_rendered_page(page_name):
    """Get prerendered page, if available."""

    rendered = None

    root_dir = pathlib.Path(__file__).parent.parent
    filename = root_dir.joinpath(cfg.RENDERED_DIR).joinpath(f"{page_name}.html")

    if filename.exists():
        with open(filename, "r") as f:
            rendered = f.read()
    return rendered


def save_rendered_page(page_name, rendered):
    """Save prerendered page."""

    root_dir = pathlib.Path(__file__).parent.parent
    filename = root_dir.joinpath(cfg.RENDERED_DIR).joinpath(f"{page_name}.html")

    with open(filename, "w") as f:
        f.write(rendered)
