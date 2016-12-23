from forum import app
from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
import requests

data = {'name' : 'L\'Oreal'}

# start of app
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', company=data)

@app.route('/admin/equipement')
def equipement():
    return render_template('equipement.html', company=data)

@app.route('/admin/restauration')
def restauration():
    return render_template('restauration.html', company=data)

@app.route('/admin/transport')
def transport():
    return render_template('transport.html', company=data)

@app.route('/admin/badges')
def badges():
    return render_template('badges.html', company=data)

@app.route('/admin/programme')
def programme():
    return render_template('programme.html', company=data)

@app.route('/admin/bon_de_commande')
def bon_de_commande():
    return render_template('bon_de_commande.html', company=data)

@app.route('/connexion', methods=["GET", "POST"])
def login():
    idf = request.form.get('id', None)
    password = request.form.get('password', None)
    if check_credentials(idf, password):
        return admin()
    else:
        return render_template('login.html')

def check_credentials(idf, password):
    return idf=="ABC" and password=="DEF"

@app.route('/send_mail', methods=["GET"])
def send_mail():
    email = request.args.get('email', 'pas_de_email')
    contact_name = request.args.get('nom_complet', 'pas_de_nom_contact')
    company_name = request.args.get('nom', 'pas_de_nom_entreprise')
    telephone = request.args.get('tel', 'pas_de_telephone')
    return _send_mail(email, contact_name, company_name, telephone)

def _send_mail(email, contact_name, company_name, telephone):
    # Create a text/plain message
    me = 'no-reply@forumorg.org'
    you = ['elmehdi.baha@gmail.com']
    #you = ['elmehdi.baha@forumorg.org', 'contact-fra@forumorg.org']
    subject = '[FRA] Demande de participation ({})'.format(company_name)
    text = """\
    Bonjour !

    Vous avez recu une nouvelle demande de participation !
    Nom du contact: {}
    Telephone: {}
    Nom de l'entreprise: {}
    Email: {}

    Cordialement,
    L'equipe Forum.
    """.format(contact_name, telephone, company_name, email)

    try:
        requests.post(
        "https://api.mailgun.net/v3/sandboxe0de963426a24a9eb4d269c82fb4987f.mailgun.org/messages",
        auth=("api", "key-64479a70e89891605fa3c663bb55c299"),
        data={"from": "no-reply <{}>".format(me),
              "to": you,
              "subject": subject,
              "text": text})
        return "Email sent."
    except:
        return "Email not sent."

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()