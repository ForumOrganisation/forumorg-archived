from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.base import MenuLink
from admin import CompanyView

import storage

import datetime
import locale
from jinja2 import Environment

# App init
app = Flask(__name__)
app.secret_key = 'supa-secret'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.add_extension('jinja2_time.TimeExtension')

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Admin Interface
admin = Admin(app, name='Interface Admin', index_view=CompanyView(storage.get_companies(), url='/admin'))
admin.add_link(MenuLink(name='Se deconnecter', url='/deconnexion'))

# Context processors
@app.context_processor
def make_price():
    def _make_price(item, qty):
        return int(item.split("(")[1].split(" ")[0]) * int(qty)
    return dict(make_price=_make_price)

# Jinja Filters
@app.template_filter('format_dt')
def format_dt(dt):
    locale.setlocale(locale.LC_ALL, "fr_FR")
    dt = datetime.datetime.strptime(dt, format("%d/%m/%Y %H:%M"))
    dt = dt.strftime("%a %d %b %H:%M")
    return dt

@app.template_filter('to_human')
def to_human(num):
    opts = {
        0: "aucun",
        1: "un",
        2: "deux",
        3: "trois",
        4: "quatre",
        5: "cinq",
        6: "six",
        7: "sept",
        8: "huit",
        9: "neuf"
    }
    return opts[num]

import views