# coding=utf-8

import json
import os
import requests

from flask import abort, redirect, render_template, request, send_from_directory, url_for, make_response
from flask_login import current_user, login_required, login_user, logout_user
from login import validate_login
from storage import Company, get_company, set_company, get_db

from forum import app, GridFS, log
from gridfs.errors import NoFile
from mailing import send_mail
from bson.objectid import ObjectId


# Admin
@app.route('/dashboard')
@app.route('/dashboard/<page>')
@login_required
def dashboard(page=None):
    if current_user.id == 'admin':
        return redirect('/admin')
    url = 'dashboard/sections/{}.html'.format(page) if page and page != "accueil" else 'dashboard/dashboard.html'
    return render_template(url)


@app.route('/connexion', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        remember_me = 'remember_me' in request.form
        company_id = request.form.get('id', None)
        password = request.form.get('password', None)
        company = get_company(company_id)
        # checking stuff out
        if not company_id or not password:
            return render_template('login.html', error="blank_fields")
        if not company:
            return render_template('login.html', error="no_company_found")
        if not validate_login(company['password'], password):
            return render_template('login.html', error="wrong_password")
        # all is good
        company = Company(id=company_id, password=password)
        print('connected_as: {}'.format(company_id))
        login_user(company, remember=remember_me)
        if company_id == "admin":
            return redirect('/admin')
        else:
            return redirect(request.args.get('next') or url_for('dashboard'))
    return render_template('login.html')


@app.route('/deconnexion')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/update_company', methods=["POST"])
@login_required
def update_company():
    page = request.form.get('page')
    if current_user.data.get(page):
        return "error"
    else:
        company = request.form.get('company')
        company = json.loads(company)
        set_company(company['id'], company)
        return "success"


@app.route('/get_resume/<oid>')
def get_resume(oid):
    try:
        file = GridFS.get(ObjectId(oid))
        response = make_response(file.read())
        response.mimetype = file.content_type
        return response
    except NoFile:
        abort(404)


@app.route('/validate_section', methods=["POST"])
@login_required
def validate_section():
    page = request.form.get('page')
    if not current_user.data.get(page):
        get_db().companies.update_one({'id': current_user.id}, {'$set': {page: True}})
        return "success"
    else:
        return "error"


@app.route('/update_banner', methods=["POST"])
@login_required
def update_banner():
    if not current_user.data.get('equipement'):
        company_id = request.form.get('pk')
        banner = request.form.get('value')

        company = get_company(company_id)
        company['banner'] = banner
        set_company(company['id'], company)
        return "success"
    else:
        abort(500)


@app.route('/add_job', methods=["POST"])
@login_required
def add_job():
    job = request.form.get('job')
    job = json.loads(job)
    get_db().jobs.insert_one(job)
    return "success"


@app.route('/remove_job', methods=["POST"])
@login_required
def remove_job():
    job_id = request.form.get('id')
    res = get_db().jobs.delete_one({'_id': ObjectId(job_id)})
    return "success"


# VITRINE
# start of app
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/send_request', methods=["GET"])
def send_request():
    # Params
    email = request.args.get('email')
    contact_name = request.args.get('nom_complet')
    company_name = request.args.get('nom')
    telephone = request.args.get('tel')
    captcha = request.args.get('captcha')

    # ReCaptcha
    base_url = 'https://www.google.com/recaptcha/api/siteverify'
    secret = os.environ.get('RECAPTCHA_SECRET_KEY')
    res = requests.post(base_url, data={'response': captcha, 'secret': secret}).json()

    # Sending mail...
    if res.get('success'):
        return send_mail(email, contact_name, company_name, telephone)
    else:
        abort(500)


# INDEXING
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
