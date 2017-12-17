from pymongo import MongoClient
import numpy as np

client = MongoClient()
db = client['INS']
authors_collection = db['authors']

exceptions = ['...']
authors_in_institute = []

for document in authors_collection.find():
    authors_in_institute.append(document['name'])

for document in authors_collection.find():
    cooperating_authors = []
    for article in document['articles']:
        for author in article['authors']:
            cooperating_authors.append(author.lstrip())

    cooperating_authors = np.unique(cooperating_authors).tolist()

    for exception in exceptions:
        if exception in cooperating_authors:
            cooperating_authors.remove(exception)

    if document['name'] in cooperating_authors:
        cooperating_authors.remove(document['name'])

    cooperating_internal_authors = []
    cooperating_external_authors = []
    for author in cooperating_authors:
        if author in authors_in_institute:
            cooperating_internal_authors.append(author)
        else:
            cooperating_external_authors.append(author)

    document.update({'internal_collaborators': cooperating_internal_authors})
    document.update({'external_collaborators': cooperating_external_authors})
    authors_collection.save(document)
