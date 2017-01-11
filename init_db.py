import os

from pymongo import MongoClient

client = MongoClient(host=os.environ.get('MONGODB_URI'))
db = client.get_default_database()

# Creating index
db.companies.create_index(keys='id', name='index_id', unique=True)

# Creating admin account
admin_data = dict(id=os.environ.get('ADMIN_ID'), password=os.environ.get('ADMIN_PASSWORD'))
try:
    db.companies.insert_one(admin_data)
except:
    print('admin already exists')
