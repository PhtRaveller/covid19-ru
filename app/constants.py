import pandas as pd
from bokeh.palettes import Reds

REGIONAL_LINKS = [{"name": "Россия", "link": "/"},
                  {"name": "Москва", "link": "/moscow"}]

# Categories
CATEGORIES = ["total", "died", "recovered", "swabs"]
CATEGORIES_STYLES = {
    "total": {"color_class": "red-font", "text": "выявлено", "icon_class": "fa-exclamation"},
    "died": {"color_class": "black-font", "text": "умерло", "icon_class": "fa-cross"},
    "recovered": {"color_class": "green-font", "text": "выздоровело", "icon_class": "fa-heart"},
    "swabs": {"color_class": "blue-font", "text": "тыс. тестов проведено", "icon_class": "fa-vial"}
    }
LEGEND_MAP = ["выявлено", "умерло", "выздоровело", "активных"]

# Swabs categories
SWABS_CATEGORIES = ["swabs_clean", "swabs_derived_daily"]
SWABS_LEGEND_MAP = ["тестов всего", "выявлено"]
SWABS_RANGE = (10000, 17000000)
SWABS_ALPHA = 25
SWABS_START_DATE = "2020-03-20"
SWABS_SIZE = 6000
SWABS_DELAY = -1

# Colors
COLOR_RAMP = ["#073763", "#990800", "#38761d", "#417ab0", "#e50b00", "#85c26b"]
MAP_PALLETE = Reds[9]
AGES_COLOR_RAMP = ["#38761d", "#417ab0", "#073763", "#e50b00", "#990800"]
DISCHARGES_COLOR_RAMP = ["#990800", "#38761d"]

# Daily plots
DAILY_LEGEND_MAP = {"18-45": "в возрасте от 18 до 45 лет",
                    "46-65": "в возрасте от 46 до 65 лет",
                    "66-79": "в возрасте от 66 до 79 лет",
                    "80+": "в возрасте старше 80 лет",
                    "children": "детей",
                    "18-45%": "в возрасте от 18 до 45 лет",
                    "46-65%": "в возрасте от 46 до 65 лет",
                    "66-79%": "в возрасте от 66 до 79 лет",
                    "80+%": "в возрасте старше 80 лет",
                    "children%": "детей",
                    "died": "умерло",
                    "recovered": "выздоровело"}
DAILY_WIDTH = pd.Timedelta(hours=16)
DAILY_DISCHARGE_CATEGORIES = ["died", "recovered"]
DAILY_RANGE = (-9000, 9000)

# Tooltips
CASES_TOOLTIP = """<div class="plot-tooltip">
    <h4>{city}</h4>
    <div>
        <span style="font-weight: bold;">Дата: </span>@date_str
    </div>"""

CASES_TOOLTIP_FOOTER = """<div>
        <span style="font-weight: bold;">{value_type}: </span>@{col}{fmt}
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
SWABS_TOOLTIP = """<div class="plot-tooltip">
    <h4>Россия</h4>
    <div>
        <span style="font-weight: bold;">Дата: </span>@date_str
    </div>
    <div>
        <span style="font-weight: bold;">Всего проведено тестов: </span>@swabs_clean{0.0a}
    </div>
    <div>
        <span style="font-weight: bold;">Проведено тестов за день: </span>@swabs_derived_daily{0.0a}
    </div>
    <div>
        <span style="font-weight: bold;">% положительных (за все время): </span>@positive{0.0 %} <div class="square" style="opacity: @alpha"></div>
    </div>
</div>
"""

DAILY_TOOLTIP_FOOTER = """<div>
        <span style="font-weight: bold;">Выявлено всего: </span>@{total_col}{{0,0}}
    </div>
    <div>
        <span style="font-weight: bold;">{value_type}: </span>@{col}{fmt}
    </div>
</div>
"""

DISCHARGES_TOOLTIP_FOOTER = """<div>
        <span style="font-weight: bold;">Выбыло: </span>@{total_col}{{0,0}}
    </div>
    <div>
        <span style="font-weight: bold;">{value_type}: </span>@{col}{fmt}
    </div>
</div>
"""

# Moscow specific
MSK_DIR = "moscow"

# Transport
MSK_TRANSPORT_DIR = "hospitals"
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

# Hospitals
MSK_HOSPITALS_DIR = "hospitals"
MSK_HOSPITALS = [{"key": "gkb40",
                  "name": "ГКБ № 40",
                  "link": "https://gkb40dzm.ru/",
                  "cmo": "Денис Николаевич Проценко",
                  "address": "ул. Сосенский стан, д. 8",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "подтверждено CoVID-19"},
                             {"key": "total_vent", "name": "на ИВЛ", "glyph": "line"},
                             {"key": "total_icu", "name": "в ОРИТ", "glyph": "line"},
                             {"key": "total_oxygen", "name": "с кислородной поддержкой", "glyph": "line"},
                             {"key": "pneumonia", "name": "внебольничная пневмония"}
                             ]
                  },
                 {"key": "gkb15",
                  "name": "ГКБ № 15 им.&nbspО.&nbspМ.&nbspФилатова",
                  "link": "http://gkb15.moscow/",
                  "cmo": "Валерий Иванович Вечорко",
                  "address": "ул. Вешняковская, д. 23",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "подтверждено CoVID-19", "glyph": "line"},
                             {"key": "total_vent", "name": "на ИВЛ", "glyph": "line"},
                             {"key": "total_icu", "name": "в ОРИТ", "glyph": "line"},
                             {"key": "total_oxygen", "name": "с кислородной поддержкой", "glyph": "line"},
                             {"key": "pneumonia", "name": "внебольничная пневмония", "glyph": "line"}
                             ]
                  },
                 {"key": "ikb2",
                  "name": "ИКБ № 2",
                  "link": "https://www.ikb2.ru/",
                  "cmo": "Светлана Васильевна Краснова",
                  "address": "8-я ул. Соколиной горы, д. 15",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "CoVID-19 (всего)", "glyph": "line"},
                             {"key": "covid_confirmed", "name": "CoVID-19 (лабораторно подтвержденных)", "glyph": "line"},
                             {"key": "covid_icu", "name": "CoVID-19 в ОРИТ", "glyph": "line"},
                             {"key": "covid_vent", "name": "CoVID-19 на ИВЛ", "glyph": "line"},
                             {"key": "covid_children", "name": "детей с CoVID-19", "glyph": "line"}
                             ]
                  },
                 {"key": "gkb50",
                  "name": "ГКБ им.&nbspС.&nbspИ.&nbspСпасокукоцкого",
                  "link": "https://50gkb.ru/",
                  "cmo": "Алексей Владимирович Погонин",
                  "address": "ул. Вучетича, д. 21",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "внебольничная пневмония + CoVID-19", "glyph": "line"},
                             {"key": "pneumonia", "name": "внебольничная пневмония", "glyph": "line"}
                             ]
                  },
                 {"key": "gkb67",
                  "name": "ГКБ № 67 им.&nbspЛ.&nbspА.&nbspВорохобова",
                  "link": "http://67gkb.ru/",
                  "cmo": "Андрей Сергеевич Шкода",
                  "address": "ул. Саляма Адиля, д. 2/44",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "подтверждено CoVID-19", "glyph": "line"},
                             {"key": "total_vent", "name": "на ИВЛ", "glyph": "line"},
                             {"key": "total_icu", "name": "в ОРИТ", "glyph": "line"}
                             ]
                  },
                 {"key": "gkbi",
                  "name": "ГКБ им.&nbspФ.&nbspИ.&nbspИноземцева",
                  "link": "https://inozemtcev.ru/",
                  "cmo": "Александр Евгеньевич Митичкин",
                  "address": "ул. Фортунатовская, д. 1",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "подтверждено CoVID-19", "glyph": "line"},
                             {"key": "total_vent", "name": "на ИВЛ", "glyph": "line"},
                             {"key": "total_icu", "name": "в ОРИТ", "glyph": "line"}
                             ]
                  },
                 {"key": "nmsc",
                  "name": "НМХЦ им.&nbspН.&nbspИ.&nbspПирогова",
                  "link": "http://www.pirogov-center.ru/",
                  "cmo": "Виталий Геннадьевич Гусаров",
                  "address": "ул. Нижняя Первомайская, д. 70",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "подтверждено CoVID-19", "glyph": "line"},
                             {"key": "total_vent", "name": "всего на ИВЛ", "glyph": "line"},
                             {"key": "total_icu", "name": "в ОРИТ", "glyph": "line"},
                             {"key": "covid_vent", "name": "подтвержденных CoVID-19 на ИВЛ", "glyph": "line"},
                             {"key": "covid_suspected", "name": "предполагаемых CoVID-19", "glyph": "line"}
                             ]
                  },
                 {"key": "mccid",
                  "name": 'МКЦИБ&nbsp"Вороновское"',
                  "link": "https://demikhova.ru/",
                  "cmo": "Сергей Николаевич Переходов",
                  "address": "Вороновское поселение, д. Голохвастово",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "подтверждено CoVID-19", "glyph": "line"},
                             {"key": "total_vent", "name": "всего на ИВЛ", "glyph": "line"},
                             {"key": "total_oxygen", "name": "с кислородной поддержкой", "glyph": "line"}
                             ]
                  },
                 ]
