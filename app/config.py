import pathlib
import pandas as pd
from bokeh.themes import Theme

DATA_DIR = "data"
GEODATA = "data/borders.geojson"
CSVDATA = "data/covid_stats.csv"
SWABSDATA = "data/swabs_rpn.csv"
SWABSDATA_CLEAN = "data/swabs_rpn_clean.csv"
RENDERED_DIR = "rendered"

ROOT_DIR = pathlib.Path(__file__).parent.parent

THEME_FILE = "static/theme.yaml"
THEME = Theme(filename=ROOT_DIR.joinpath(THEME_FILE))

MAX_MAIN_HEIGHT = 400
MAX_MAIN_WIDTH = 600
DATE_WIDTH = pd.Timedelta(hours=12)
MAP_BREEZE = 0.05
