import json
import os

import pymongo

MONGODB_URL = os.environ.get('MONGODB_URL')
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
MONGODB_PWD = os.environ.get('MONGODB_PWD')
MONGODB_URI = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PWD}@{MONGODB_URL.split('//')[1]}?retryWrites=true&w=majority"

FILE_PATH = os.environ.get('FILE_PATH')
DATABASE_NAME = 'pictograms'
COLLECTION_NAME = 'pictograms'
INDEX_NAME = 'keywords.keyword_1'

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

db[COLLECTION_NAME].create_index([('keywords.keyword', pymongo.ASCENDING)], name=INDEX_NAME)
print('Index created successfully')
