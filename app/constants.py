from bokeh.palettes import Reds

REGIONAL_LINKS = [{"name": "Россия", "link": "/"},
                  {"name": "Москва", "link": "/moscow"},]

CATEGORIES = ["total", "died", "recovered", "swabs"]
CATEGORIES_STYLES = {
    "total": {"color_class": "red-font", "text": "выявлено", "icon_class": "fa-exclamation"},
    "died": {"color_class": "black-font", "text": "умерло", "icon_class": "fa-cross"},
    "recovered": {"color_class": "green-font", "text": "выздоровело", "icon_class": "fa-heart"},
    "swabs": {"color_class": "blue-font", "text": "тыс. тестов проведено", "icon_class": "fa-vial"}
    }

LEGEND_MAP = ["выявлено", "умерло", "выздоровело"]
COLOR_RAMP = ["#073763", "#990800", "#38761d", "#02607a", "#b02a09", "#658c1c"]
MAP_PALLETE = Reds[9]

# Moscow specific
# Transport
PUBLIC_TR_COLS = [
    {"key": "metro", "name": "метро"},
    {"key": "landlines", "name": "наземный транспорт"},
    {"key": "intercity trains", "name": "электрички"}
    ]
PRIVATE_TR_COLS = [
    {"key": "taxi", "name": "такси"},
    {"key": "car sharing", "name": "каршеринг"},
    {"key": "cars", "name": "личные автомобили"}
    ]
