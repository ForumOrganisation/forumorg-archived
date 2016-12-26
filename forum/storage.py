from pymongo import MongoClient
import os
import json

if os.environ.get('env') == 'dev':
	def get_company(company_id):
		fn = os.path.join(os.path.dirname(__file__), '..', 'sample.json')
		with open(fn) as data_file:
			data = json.load(data_file)
			return data
else:
	client = MongoClient(host=os.environ.get('MONGODB_URI'))
	db = client.heroku_lx65hjrq

	def get_company(company_id):
		return db.companies.find_one({"id": company_id})
