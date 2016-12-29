from pymongo import MongoClient
import os
import json


client = MongoClient(host=os.environ.get('MONGODB_URI'))
db = client.heroku_lx65hjrq
# Creating admin account
admin_doc = {'id': os.environ.get('ADMIN_ID'), 'name': 'Administrateur', 'password': os.environ.get('ADMIN_PASSWORD')}
db.companies.replace_one({'id': admin_doc['id']}, admin_doc, upsert=True)

def get_company(company_id):
	company = db.companies.find_one({'id': company_id})
	# dropping unserializable field
	if company:
		company.pop('_id', None)
	return company

def set_company(company_id, company):
	return db.companies.replace_one({'id': company_id}, company, upsert=True)

def get_companies():
	return db.companies