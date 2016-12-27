# coding: utf-8

from flask import Flask
from flask_login import LoginManager
import datetime
import locale
from jinja2 import Environment

app = Flask(__name__)
app.secret_key = 'supa-secret'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.add_extension('jinja2_time.TimeExtension')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.template_filter('format_dt')
def format_dt(dt):
	locale.setlocale(locale.LC_ALL, "fr_FR")
	dt = datetime.datetime.strptime(dt, format("%d/%m/%Y %H:%M"))
	dt = dt.strftime("%a %d %b %H:%M")
	return dt

@app.template_filter('to_human')
def to_human(num):
	opts = {
		"1": "un",
		"2": "deux",
		"3": "trois",
		"4": "quatre",
		"5": "cinq",
		"6": "six",
		"7": "sept",
		"8": "huit",
		"9": "neuf",
	}
	return opts[num]

import views