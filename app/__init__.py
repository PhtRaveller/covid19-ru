from flask import Flask

app = Flask(__name__,
            static_folder="../static",
            template_folder="../static/templates")
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

from app import routes
