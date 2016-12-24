from forum import app
from flask import Flask, render_template, request, url_for, redirect
import smtplib
from email.mime.text import MIMEText
import requests
from storage import check_credentials, get_company
from mailing import send_mail

data = {}

# start of app
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', company=data)

@app.route('/admin/<page_name>')
def get_page(page_name):
    return render_template('{}.html'.format(page_name), company=data)

@app.route('/connexion', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        idf = request.form.get('id', None)
        password = request.form.get('password', None)
        if check_credentials(idf, password):
            data = get_company(idf)
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/send_request', methods=["GET"])
def send_request():
    email = request.args.get('email', 'pas_de_email')
    contact_name = request.args.get('nom_complet', 'pas_de_nom_contact')
    company_name = request.args.get('nom', 'pas_de_nom_entreprise')
    telephone = request.args.get('tel', 'pas_de_telephone')
    return mailing.send_mail(email, contact_name, company_name, telephone)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()