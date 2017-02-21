# coding=utf-8

import os
import json
import csv

from flask_script import Manager
from pymongo import MongoClient
from forum import app, log
import wget
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Personalization, Substitution
from flask_assets import ManageAssets

client = MongoClient(host=os.environ.get('MONGODB_URI'))
db = client.get_default_database()

manager = Manager(app)
manager.add_command("assets", ManageAssets())


@manager.command
def batch_emails():
    users = db.users.find({'events.fra.ambassador': {'$exists': True}})
    users = [user['id'] for user in users]
    recipients = users
    total = len(users)
    sent = 0
    failed = 0
    me = 'ambassadeur2017@forumorg.org'
    subject = u'Forum Rhone-Alpes: Ambassadeur'
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    for r in recipients:
        mail = Mail()
        mail.set_from(Email(me))
        mail.set_template_id('e449ac1c-51a2-485e-9275-7031f10d490f')
        personalization = Personalization()
        personalization.add_to(Email(r))
        mail.add_personalization(personalization)
        mail.personalizations[0].add_substitution(Substitution("-subject-", subject))
        try:
            sg.client.mail.send.post(request_body=mail.get())
            print(r)
            print("{} mails restants".format(total - sent))
            sent += 1
        except:
            failed += 1
    print("Statistics: sent({}), failed({})".format(sent, failed))


@manager.command
def split_companies():
    fs = os.path.join(os.path.dirname(__file__), 'data/si.csv')
    fe = os.path.join(os.path.dirname(__file__), 'data/ecoles.csv')
    fs = open(fs).read()
    fe = open(fe).read()
    cur = db.companies.find({})
    for doc in cur:
        if doc['id'] in fs:
            pole = 'si'
        elif doc['id'] in fe:
            pole = 'school'
        else:
            pole = 'fra'
        if doc['id'] != 'admin':
            db.companies.update_one({'_id': doc['_id']}, {'$set': {'pole': pole}}, upsert=True)


@manager.command
def fix_users():
    db.users.update_many({'events.fra': None}, {'$set': {'events.fra.registered': False}})


@manager.command
def change_users():
    cur = db.users.find({})
    for doc in cur:
        if doc['id'] != doc['id'].lower():
            print(doc)


@manager.command
def update_companies():
    new = wget.download(os.environ.get('NEW_URL'), 'data/new.csv')
    fn = os.path.join(os.path.dirname(__file__), 'data/new.csv')
    with open(fn, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            db.companies.update_one({'id': row[0]}, {'$set': {'password': row[1]}})


@manager.command
def create_events_fra():
    fn = os.path.join(os.path.dirname(__file__), 'data/events_fra.json')
    with open(fn, 'r') as f:
        data = json.loads(f.read())
        db.events.insert(data)


@manager.command
def create_furnitures():
    db.drop_collection('furnitures')
    db.create_collection('furnitures', capped=True, size=20480)
    fn = os.path.join(os.path.dirname(__file__), 'data/furnitures.json')
    with open(fn, 'r') as f:
        data = json.loads(f.read())
        db.furnitures.insert(data, check_keys=False)


@manager.command
def create_fra():
    db.users.update_many({}, {'$set': {'events.fra': {'registered': False}}})


@manager.command
def create_mastere_class():
    db.users.update_many({}, {'$set': {'events.master_class': {'registered': False}}})


@manager.command
def create_styf():
    db.events.insert_one({'name': 'styf', 'quota': 50, 'places_left': 50})
    db.users.update_many({}, {'$set': {'events.styf': {}}})


@manager.command
def create_joi():
    fn = os.path.join(os.path.dirname(__file__), 'data/events.db')
    events = open(fn).read()
    events = events.split('\n')
    confs = [e.split(' - ') for e in events[:7]]
    tables = events[7:][:-1]
    for c in confs:
        db.events.insert_one({'name': c[0], 'type': 'conference', 'quota': int(c[1]), 'places_left': int(c[1])})
    for t in tables:
        db.events.insert_one({'name': t, 'quota': 30, 'type': 'table_ronde', 'places_left': {'first': 30, 'second': 30}})
    db.users.update_many({}, {'$set': {'events.joi': {}}})


@manager.command
def create_indexes():
    db.users.create_index(keys='id', name='index_id', unique=True)
    db.companies.create_index(keys='id', name='index_id', unique=True)


@manager.command
def create_admin():
    db.companies.update_one({'id': 'admin'}, {'$set': {'password': os.environ.get('ADMIN_PASSWORD')}}, upsert=True)


if __name__ == "__main__":
    manager.run()
