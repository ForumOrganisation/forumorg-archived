import datetime
import locale
import os

from flask import Flask
from flask_admin import Admin
from flask_admin.base import MenuLink
from flask_login import LoginManager

from admin import CompanyView, EventView, UserView
<<<<<<< HEAD
from storage import get_companies, get_events, get_users, init_storage, get_jobs
=======
from storage import get_companies, get_events, get_users, init_storage, get_styf
>>>>>>> 23159615ded7fa3162dcfb266913b97b0b2e30c2

# App init
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or 'my-debug-key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.add_extension('jinja2_time.TimeExtension')

# Storage init
init_storage()

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Admin Interface
admin = Admin(app, name='Interface Admin', index_view=CompanyView(get_companies(), url='/admin'))
admin.add_view(UserView(get_users()))
admin.add_view(EventView(get_events()))
admin.add_view(EventView(get_styf()))
admin.add_link(MenuLink(name='Se deconnecter', url='/deconnexion'))

# Jinja Filters
@app.template_filter('to_jobs')
def to_jobs(company_id):
    # return list(get_jobs().find({'company_id': company_id}))
    return [{'id': 'amazon', 'title': 'TITLE_JOB TITLE_JOB TITLE_JOB (M/F)', 'type': 'Stage', 'duration': '6 mois',
            'description': 'zeaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaae', 'locations': ['Paris', 'New York', 'SF']}]


@app.template_filter('format_dt')
def format_dt(dt):
    try:
        locale.setlocale(locale.LC_ALL, "fr_FR")
    except:  # heroku shitteries
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
        9: "neuf",
        10: "dix",
        11: "onze",
        12: "douze"
    }
    return opts[num]


@app.template_filter('empty_furnitures')
def empty_furniture(f):
    return sum([v['quantity'] for k, v in f.items()]) == 0


@app.template_filter('empty_events')
def empty_events(e):
    return any([v['registered'] for k, v in e.items()])


@app.template_filter('empty_dishes')
def empty_dishes(d):
    return sum([sum(a.values()) for a in d.values()]) == 0


import views
