from pymongo import MongoClient
import os
import json

db = None

def init_storage():
	global db
	client = MongoClient(host=os.environ.get('MONGODB_URI'))
	db = client.get_default_database()
	# Making sure admin account is created
	admin_doc = {'name': 'Administrateur', 'id': os.environ.get('ADMIN_ID'), 'password': os.environ.get('ADMIN_PASSWORD')}
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