import json
import os

import pymongo

MONGODB_URI = os.environ.get('MONGODB_URI')

FILE_PATH = os.environ.get('FILE_PATH')
DATABASE_NAME = 'pictograms'
COLLECTION_NAME = 'pictograms'

db = pymongo.MongoClient(MONGODB_URI)[DATABASE_NAME]

skip_data_insertion = False
if db[COLLECTION_NAME].count_documents({}) > 0:
    print('Data already exists in the database')
    skip_data_insertion = True

if not skip_data_insertion:
    with open(FILE_PATH, 'r') as f:
        jsonData = json.load(f)
        db[COLLECTION_NAME].insert_many(jsonData)
    print('Data inserted successfully')

db[COLLECTION_NAME].create_index([('keywords.keyword', pymongo.ASCENDING)], name='keywords.keyword_1')
db[COLLECTION_NAME].create_index([('keywords.plural', pymongo.ASCENDING)], name='keywords.plural_1')
print('Indexes created successfully')
