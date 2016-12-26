from pymongo import MongoClient
import os
import json

fn = os.path.join(os.path.dirname(__file__), '..', 'sample.json')
with open(fn) as data_file:
	data = json.load(data_file)

if os.environ.get('env') == 'dev':
	def get_company(company_id):
		return data	
else:
	client = MongoClient(host=os.environ.get('MONGODB_URI'))
	db = client.heroku_lx65hjrq
	try:
		db.companies.insert_one(data)
	except:
		print("Oups. Already created.")

	def get_company(company_id):
		return db.companies.find_one({"id": company_id})
