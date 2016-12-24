import requests

def send_mail(email, contact_name, company_name, telephone):
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