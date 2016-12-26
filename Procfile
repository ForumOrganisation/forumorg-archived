web: gunicorn forum:app
init: mongoimport -v --db heroku_lx65hjrq --collection companies --file sample.json --upsert --upsertFields=idf
db: sudo mongod
dev: python ./runserver.py
