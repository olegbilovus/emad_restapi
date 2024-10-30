import json
import os

import pymongo

MONGODB_URI = os.environ.get('MONGODB_URI')

JSONS_DIR = os.environ.get('JSONS_DIR')
DATABASE_NAME = 'pictograms'
COLLECTION_NAME = 'pictograms'

FILES_PATH = [os.path.join(JSONS_DIR, f) for f in os.listdir(JSONS_DIR) if f.endswith('.json')]

db = pymongo.MongoClient(MONGODB_URI)[DATABASE_NAME]

skip_data_insertion = False
if db[COLLECTION_NAME].count_documents({}) > 0:
    print('Data already exists in the database')
    skip_data_insertion = True

pictograms = {}
langs = []
if not skip_data_insertion:
    for i, file in enumerate(FILES_PATH):
        with open(file, 'r', encoding="utf8") as f:
            jsonData = json.load(f)
            lang = f.name.split(os.sep)[-1].split('.')[0]
            langs.append(lang)
            for data in jsonData:
                if i == 0:
                    pictograms[data['_id']] = {
                        '_id': data['_id'],
                        'sex': data['sex'],
                        'violence': data['violence'],
                        'keywords': {
                            lang: data['keywords']
                        }
                    }
                else:
                    try:
                        pictograms[data['_id']]['keywords'][lang] = data['keywords']
                    except KeyError:
                        pictograms[data['_id']] = {
                            '_id': data['_id'],
                            'sex': data['sex'],
                            'violence': data['violence'],
                            'keywords': {
                                lang: data['keywords']
                            }
                        }
    db[COLLECTION_NAME].insert_many(list(pictograms.values()))
    print('Data inserted successfully')

for lang in langs:
    lang_key = f'keywords.{lang}'
    db[COLLECTION_NAME].create_index([(f'{lang_key}.keyword', pymongo.ASCENDING)], name=f'{lang_key}.keyword_1')
    db[COLLECTION_NAME].create_index([(f'{lang_key}.plural', pymongo.ASCENDING)], name=f'{lang_key}.plural_1')
print('Indexes created successfully')
