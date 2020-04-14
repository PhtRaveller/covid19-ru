from flask import Flask

covid_app = Flask(__name__,
            static_folder="../static",
            template_folder="../static/templates")
covid_app.jinja_env.auto_reload = True
covid_app.config['TEMPLATES_AUTO_RELOAD'] = True

from app import routes
