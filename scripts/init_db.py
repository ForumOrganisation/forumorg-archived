import os

from pymongo import MongoClient


def main():
    try:
        client = MongoClient(host=os.environ.get('MONGODB_URI'))
        db = client.get_default_database()
        # tasks
        # db.users.create_index(keys='id', name='index_id', unique=True)
        # create_admin(db)
        db.users.update_many({'$or': [{'events.joi.conference.registered': True}, {'events.joi.table_ronde.registered': True}]},
        {'$set': {'events.joi.registered': True}})
    except Exception as e:
        print(e)


def create_admin(db):
    admin_data = dict(id=os.environ.get('ADMIN_ID'), password=os.environ.get('ADMIN_PASSWORD'))
    try:
        db.companies.insert_one(admin_data)
    except:
        print('admin already exists')


if __name__ == '__main__':
    main()
