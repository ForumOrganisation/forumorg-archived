from pymongo import MongoClient
import os
import json

fn = os.path.join(os.path.dirname(__file__), '..', 'companies.json')
with open(fn) as file:
	data = json.load(file)

client = MongoClient(host=os.environ.get('MONGODB_URI'))
db = client.heroku_lx65hjrq
for c in data['companies']:
	db.companies.replace_one({'id': c['id']}, c, upsert=True)

def get_company(company_id):
	company = db.companies.find_one({'id': company_id})
	if company:
		company.pop('_id', None)
	return company

def set_company(company_id, company):
	return db.companies.replace_one({'id': company_id}, company, upsert=True)

def get_companies():
	return db.companies