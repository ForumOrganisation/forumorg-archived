from __future__ import print_function
import datetime
import locale
import os
import sys

from flask import Flask, request, url_for
from flask_admin import Admin
from flask_admin.base import MenuLink
from flask_login import LoginManager
from gridfs import GridFS
from flask_babelex import Babel
from collections import OrderedDict, defaultdict

from admin import CompanyView, EventView, UserView, StatisticsView, JobView
from storage import init_storage, get_db

# App init
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or 'my-debug-key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.add_extension('jinja2_time.TimeExtension')

# Storage init
init_storage()
GridFS = GridFS(get_db(), collection='resumes')

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Babel
babel = Babel(app)

import assets


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['fr', 'en'])


# Admin Interface
admin = Admin(app, name='Interface Admin', index_view=CompanyView(get_db().companies, url='/admin'))
admin.add_view(UserView(get_db().users))
admin.add_view(EventView(get_db().events))
admin.add_view(JobView(get_db().jobs))
admin.add_view(StatisticsView(name='Stats', endpoint='stats'))
admin.add_link(MenuLink(name='Se deconnecter', url='/deconnexion'))


@app.context_processor
def get_furnitures():
    def _get_furnitures():
        return list(get_db().furnitures.find({}, {'_id': False}))
    return dict(get_furnitures=_get_furnitures)


@app.context_processor
def get_events():
    def _get_events():
        return list(get_db().events.find({}, {'_id': False}))
    return dict(get_events=_get_events)


@app.context_processor
def get_resumes():
    def _get_resumes():
        users = list(get_db().users.find({'profile.resume_id': {'$ne': None}}, {'profile': 1}))
        users = [u['profile'] for u in users]
        for u in users:
            u['resume_url'] = url_for('get_resume', oid=u.pop('resume_id', None))
            u.pop('_id', None)
        return users
    return dict(get_resumes=_get_resumes)


@app.context_processor
def get_stats():
    def _get_stats():
        result = defaultdict(dict)
        for s in ['equipement', 'restauration', 'badges', 'transport', 'programme']:
            cur = get_db().companies.aggregate([{'$skip': 1}, {'$group': {'_id': '$pole', 'all': {'$sum': 1}, 'validated': {'$sum': {'$cmp': ['${}'.format(s), False]}}}}])
            for c in cur:
                pole, total, validated = c['_id'], c['all'], c['validated']
                result[pole][s] = round(100.0 * validated / total, 2)
        for k, v in result.items():
            result[k] = OrderedDict(sorted(v.items()))
        result = OrderedDict(sorted(result.items()))
        return result
    return dict(get_stats=_get_stats)


# Jinja Filters
@app.template_filter('to_jobs')
def to_jobs(company_id):
    jobs = list(get_db().jobs.find({'company_id': company_id}))
    for j in jobs:
        j['_id'] = str(j['_id'])
    return jobs


@app.template_filter('to_furniture')
def to_furniture(furniture_id):
    return get_db().furnitures.find_one({'id': furniture_id})


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


@app.template_filter('to_days')
def to_days(duration):
    opts = {
        "wed": "Mercredi",
        "thu": "Jeudi",
        "both": "Mercredi & Jeudi"
    }
    return opts[duration]


@app.template_filter('to_size')
def to_size(size):
    return int(size) if float(size).is_integer() else float(size)


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


@app.template_filter('nb_dishes')
def nb_dishes(size):
    if size <= 12:
        return 2
    elif 12 < size <= 18:
        return 4
    elif size > 18:
        return 6


@app.template_filter('empty_furnitures')
def empty_furniture(f):
    return sum(f.values()) == 0


@app.template_filter('empty_events')
def empty_events(e):
    return any(e.values())


@app.template_filter('empty_dishes')
def empty_dishes(d):
    return sum([sum(a.values()) for a in d.values()]) == 0


def log(m):
    print(m, file=sys.stderr)


import views
