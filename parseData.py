import re
import os
import pprint
import bibtexparser
from pymongo import MongoClient

client = MongoClient()
db = client['INS']
authors_collection = db['authors']

authors_dict = dict()
DATA_DIR = './data/'
for filename in os.listdir(DATA_DIR):
    publications_array = []

    with open(DATA_DIR + filename) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

        for publication in bib_database.entries:
            publications_array.append({'author': publication['author'], 'year': publication['year']})

    authors_dict[filename[:-4]] = publications_array
    authors_collection.insert_one({'name': 'filename[:-4]', 'publications': publications_array})

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(authors_dict)
