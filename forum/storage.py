from pymongo import MongoClient
import os

client = MongoClient(host=os.environ.get('MONGODB_URI'))
db = client.heroku_lx65hjrq
# inserting placeholder
db.companies.delete_many({})
db.companies.insert_one({"name": "Amazon", "idf": "AMAZON", "password": "amazon"})
db.companies.insert_one({"name": "SNCF", "idf": "SNCF", "password": "sncf"})

def check_credentials(idf, password):
    company = db.companies.find_one({"idf": idf})
    if company and company["password"] == password:
    	return True
    else:
    	return False

def get_company(idf):
	return db.companies.find_one({"idf": idf})