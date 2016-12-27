from pymongo import MongoClient
import os
import json

fn = os.path.join(os.path.dirname(__file__), '..', 'sample.json')
with open(fn) as data_file:
	data = json.load(data_file)

if os.environ.get('env') == 'dev':
	def get_company(company_id):
		return data["company"]

	def set_company(company):
		with open(fn, 'w') as data_file:
			company = json.dumps(dict(company=company), indent=4)
			data_file.write(company)
else:
	client = MongoClient(host=os.environ.get('MONGODB_URI'))
	db = client.heroku_lx65hjrq
	db.companies.replace_one({"id": data["company"]["id"]}, data["company"], upsert=True)

	def get_company(company_id):
		company = db.companies.find_one({"id": company_id})
		company.pop("_id", None) # dropping unserializable bitch
		return company

	def set_company(company):
		return db.companies.replace_one({"id": company["id"]}, company, upsert=True)
