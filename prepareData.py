from pymongo import MongoClient
import numpy as np
import bson

client = MongoClient()
db = client['INS']
authors_collection = db['authors']

exceptions = ['...', 'J ...']
authors_in_institute = []

for document in authors_collection.find():
    authors_in_institute.append(document['name'])

for document in authors_collection.find():
    cooperating_authors = []
    for article in document['articles']:
        for author in article['authors']:
            if author not in exceptions:
                cooperating_authors.append(author.lstrip())

    unique, counts = np.unique(cooperating_authors, return_counts=True)
    cooperating_authors = dict(zip(unique, counts))

    cooperating_internal_authors = dict()
    cooperating_external_authors = dict()
    for key, value in cooperating_authors.items():
        if key in authors_in_institute:
            cooperating_internal_authors[key] = value
        else:
            cooperating_external_authors[key] = value

    internal_collaborators = {k: bson.Int64(v) for k, v in cooperating_internal_authors.items()}
    external_collaborators = {k: bson.Int64(v) for k, v in cooperating_external_authors.items()}

    document.update({'internal_collaborators': internal_collaborators})
    document.update({'external_collaborators': external_collaborators})
    authors_collection.save(document)
