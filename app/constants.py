from bokeh.palettes import Reds

REGIONAL_LINKS = [{"name": "Россия", "link": "/"},
                  {"name": "Москва", "link": "/moscow"}]

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
                             {"key": "pneumonia", "name": "внебольничная пневмония"},
                             {"key": "total_icu", "name": "в ОРИТ", "glyph": "line"},
                             {"key": "total_vent", "name": "на ИВЛ", "glyph": "line"}
                             ]
                  },
                 {"key": "gkb15",
                  "name": "ГКБ № 15 им. О. М. Филатова",
                  "link": "http://gkb15.moscow/",
                  "cmo": "Валерий Иванович Вечорко",
                  "address": "ул. Вешняковская, д. 23",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "подтверждено CoVID-19", "glyph": "line"},
                             {"key": "pneumonia", "name": "внебольничная пневмония", "glyph": "line"},
                             {"key": "total_icu", "name": "в ОРИТ", "glyph": "line"},
                             {"key": "total_vent", "name": "на ИВЛ", "glyph": "line"}]
                  },
                 {"key": "ikb2",
                  "name": "ИКБ № 2",
                  "link": "https://www.ikb2.ru/",
                  "cmo": "Светлана Васильевна Краснова",
                  "address": "8-я ул. Соколиной горы, д. 15",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "подтверждено CoVID-19", "glyph": "line"},
                             {"key": "covid_children", "name": "детей с CoVID-19", "glyph": "line"},
                             {"key": "covid_icu", "name": "подтвержденных CoVID-19 в ОРИТ", "glyph": "line"},
                             {"key": "covid_vent", "name": "подтвержденных CoVID-19 на ИВЛ", "glyph": "line"},
                             {"key": "total_vent", "name": "всего на ИВЛ", "glyph": "line"}]
                  },
                 {"key": "gkb67",
                  "name": "ГКБ № 67 им. Л. А. Ворохобова",
                  "link": "http://67gkb.ru/",
                  "cmo": "Андрей Сергеевич Шкода",
                  "address": "ул. Саляма Адиля, д. 2/44",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "подтверждено CoVID-19", "glyph": "line"},
                             {"key": "total_icu", "name": "в ОРИТ", "glyph": "line"},
                             {"key": "total_vent", "name": "на ИВЛ", "glyph": "line"}]
                  },
                 {"key": "nmsc",
                  "name": "НМХЦ им. Н. И. Пирогова",
                  "link": "http://www.pirogov-center.ru/",
                  "cmo": "Виталий Геннадьевич Гусаров",
                  "address": " ул. Нижняя Первомайская, д. 70",
                  "fields": [{"key": "total", "name": "всего на лечении", "glyph": "bar", "alpha": 0.25},
                             {"key": "covid", "name": "подтверждено CoVID-19", "glyph": "line"},
                             {"key": "covid_suspected", "name": "предполагаемых CoVID-19", "glyph": "line"},
                             {"key": "total_icu", "name": "в ОРИТ", "glyph": "line"},
                             {"key": "covid_vent", "name": "подтвержденных CoVID-19 на ИВЛ", "glyph": "line"},
                             {"key": "total_vent", "name": "всего на ИВЛ", "glyph": "line"}]
                  },
                 ]
