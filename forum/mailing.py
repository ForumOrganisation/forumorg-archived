import sendgrid
import os
from sendgrid.helpers.mail import *

def send_mail(email, contact_name, company_name, telephone):
    # Create a text/plain message
    me = 'no-reply@forumorg.org'
    you = 'elmehdi.baha@forumorg.org'
    #you = 'contact-fra@forumorg.org'
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

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    # Setting from, subject, content, reply to
    from_email = Email(me)
    to_email = Email(you)
    content = Content('text/plain', text)
    mail = Mail(from_email, subject, to_email, content)
    # Adding bcc
    mail.personalizations[0].add_bcc(Email('elmehdi.baha@gmail.com'))
    #mail.personalizations[0].add_bcc(Email('elmehdi.baha@forumorg.org'))
    # Sending email
    print("Sending email from {}...".format(company_name))
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print("Email sent: {}".format(response.body))
        return 'Email sent.'
    except:
        return 'Email not sent.'