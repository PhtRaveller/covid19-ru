from bokeh.palettes import Reds

REGIONAL_LINKS = [{"name": "Москва", "link": "/moscow"},
                  {"name": "Московская область", "link": "/mo"},
                  {"name": "Санкт-Петербург", "link": "/spb"}]
CATEGORIES = ["total", "died", "recovered", "swabs"]
CATEGORIES_STYLES = {
    "total": {"color_class": "red-font", "text": "выявлено", "icon_class": "fa-exclamation"},
    "died": {"color_class": "black-font", "text": "умерло", "icon_class": "fa-cross"},
    "recovered": {"color_class": "green-font", "text": "выздоровело", "icon_class": "fa-heart"},
    "swabs": {"color_class": "blue-font", "text": "тыс. тестов проведено", "icon_class": "fa-vial"}
    }
DEFAULT_TITLE = "<h4>Статистика случаев</h4>"
LEGEND_MAP = ["выявлено", "умерло", "выздоровело"]
COLOR_RAMP = ["#073763", "#990800", "#38761d"]
MAP_PALLETE = Reds[9]
