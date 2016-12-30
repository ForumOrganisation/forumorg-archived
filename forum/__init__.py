from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.base import MenuLink
from admin import CompanyView

from storage import init_storage, get_companies

import datetime
import locale
from jinja2 import Environment

# Storage init
init_storage()

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
admin = Admin(app, name='Interface Admin', index_view=CompanyView(get_companies(), url='/admin'))
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
    try:
        locale.setlocale(locale.LC_ALL, "fr_FR")
    except: # heroku shitteries
        locale.setlocale(locale.LC_ALL, "fr_FR.utf8")

    try:
        dt = datetime.datetime.strptime(dt, format("%d/%m/%Y %H:%M"))
        dt = dt.strftime("%a %d %b %H:%M")
    except:
        print('Error in datetime formatting')
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

@app.template_filter('empty_furniture')
def empty_furniture(f):
    return sum([v['quantity'] for k,v in f.items()]) == 0

@app.template_filter('empty_events')
def empty_events(e):
    return any([v['registered'] for k,v in e.items()])

@app.template_filter('empty_dishes')
def empty_dishes(d):
    return sum(d.values()) == 0

import views