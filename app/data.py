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


def get_region_data(all_data, region):
    """Extract data for `region`. Note, that `all_data` is assumed to be sorted by date in ascending order."""

    region_data = all_data.iloc[-1][region]
    region_diff_data = all_data.diff().iloc[-1][region]
