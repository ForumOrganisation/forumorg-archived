import os

import flask_login

from pymongo import MongoClient

db = None

def init_storage():
    global db
    client = MongoClient(host=os.environ.get('MONGODB_URI'))
    db = client.get_default_database()
    # Creating index
    db.companies.create_index(keys='id', name='index_id', unique=True)
    # Creating admin account
    create_admin()

def get_company(company_id):
    company = db.companies.find_one({'id': company_id})
    company.pop('_id', None) if company else None
    return company

def set_company(company_id, company_data):
    return db.companies.replace_one({'id': company_id}, company_data)

def get_companies():
    return db.companies

def create_admin():
    admin_data = dict(id=os.environ.get('ADMIN_ID'), password=os.environ.get('ADMIN_PASSWORD'))
    db.companies.replace_one({'id': admin_data['id']}, admin_data, upsert=True)

class Company(flask_login.UserMixin):

    def __init__(self, id, password=None, data=None):
        self.id = id
        self.password = password
        self.data = data

    def get_id(self):
        return self.id
