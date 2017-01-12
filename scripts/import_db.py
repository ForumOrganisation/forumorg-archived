from bson import BSON, decode_all
from pymongo import MongoClient
import os


client = MongoClient(os.environ.get('MONGODB_URI'))
db = client.get_default_database()
users, events, companies = db.users, db.events, db.companies

with open('backup/heroku_lx65hjrq/users.bson', 'rb') as f:
    users.insert(decode_all(f.read()))

with open('backup/heroku_lx65hjrq/companies.bson', 'rb') as f:
    companies.insert(decode_all(f.read()))

with open('backup/heroku_lx65hjrq/events.bson', 'rb') as f:
    events.insert(decode_all(f.read()))
