import os
import json
import csv

from flask_script import Manager
from pymongo import MongoClient
from forum import app
import wget

manager = Manager(app)
client = MongoClient(host=os.environ.get('MONGODB_URI'))
db = client.get_default_database()


@manager.command
def fix_users():
    db.users.update_many({'events.fra': None}, {'$set': {'events.fra.registered': False}})


@manager.command
def change_users():
    cur = db.users.find({})
    for doc in cur:
        try:
            if doc['id'] != doc['id'].lower():
                print(doc)
            # db.users.update_one({'_id': doc['_id']}, {'$set': {'id': doc['id'].lower()}})
        except:
            pass


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
