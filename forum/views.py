from flask import Flask, render_template, request, url_for, redirect
from forum import login_manager
from flask_login import login_user, login_required, logout_user

from forum import app
from company import Company
from storage import get_company
from mailing import send_mail
from company import validate_login

######### ADMIN ###########

@app.route('/admin')
@app.route('/admin/<page>')
@login_required
def admin(page=None):
    # asking for specific page
    if page:
        return render_template('{}.html'.format(page))
    # default option is main dashboard
    else:
        return render_template('admin.html')

@app.route('/connexion', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        remember_me = 'remember_me' in request.form
        company_id = request.form.get('id', None)
        password = request.form.get('password', None)
        company = get_company(company_id)
        # checking stuff out
        if not company_id or not password:
            return render_template('login.html', error= "blank_fields")
        if not company:
            return render_template('login.html', error="no_company_found")
        if not validate_login(company['password'], password):
            return render_template('login.html', error="wrong_password")
        # all is good
        company = Company(company_id, password, data=company)
        login_user(company, remember=remember_me)
        return redirect(request.args.get('next') or url_for('admin'))
    return render_template('login.html')

@app.route('/deconnexion')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

######### VITRINE ###########

# start of app
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/send_request', methods=["GET"])
def send_request():
    email = request.args.get('email', 'pas_de_email')
    contact_name = request.args.get('nom_complet', 'pas_de_nom_contact')
    company_name = request.args.get('nom', 'pas_de_nom_entreprise')
    telephone = request.args.get('tel', 'pas_de_telephone')
    return send_mail(email, contact_name, company_name, telephone)
