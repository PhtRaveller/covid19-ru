from flask import render_template
from app import app
from app import data

@app.route("/")
def index():
    """Main page of the dashboard."""
    city = "Россия"
    main_links = [{"name": "Больницы", "link": "#hospitals"},
                  {"name": "Транспорт", "link": "#transport"}]
    secondary_links = [{"name": "Санкт-Петербург", "link": "/spb"},
                       {"name": "Московская область", "link": "/mo"}]
    stats = [{"color_class": "red-font", "value": 11221, "diff": 223, "text": "выявлено", "icon_class": "fa-exclamation"},
             {"color_class": "black-font", "value": 112, "diff": 5, "text": "умерло", "icon_class": "fa-cross"},
             {"color_class": "green-font", "value": 454, "diff": 54, "text": "выздоровело", "icon_class": "fa-heart"},
             {"color_class": "blue-font", "value": 1130, "diff": 54, "text": "тыс. тестов проведено", "icon_class": "fa-vial"},]
    return render_template("stats.html", city=city,
                           main_links=main_links, secondary_links=secondary_links,
                           stats=stats)
