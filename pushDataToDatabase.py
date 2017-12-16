import os
import json
from pymongo import MongoClient

client = MongoClient()
db = client['INS']
authors_collection = db['authors']

authors_dict = dict()
DATA_DIR = './authors/'
for filename in os.listdir(DATA_DIR):
    data = json.load(open(DATA_DIR + filename))
    authors_collection.insert_one(data)
