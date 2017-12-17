from pymongo import MongoClient
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np


def draw_plot(collection, title, file_name, count):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if count != 0:
        collection = collection[-count:]

    authors_labels, ys, xs = [], [], []
    index = 0
    for authors, x in collection:
        ys.append(index)
        authors_labels.append(authors)
        xs.append(x)
        index += 1

    ax.barh(ys, xs)
    plt.title(title)
    plt.yticks(ys, authors_labels)
    plt.tight_layout()
    fig.savefig(file_name)


def collaborators_by_decade(decade):
    client = MongoClient()
    db = client['INS']
    authors_collection = db['authors']

    exceptions = ['...']
    authors_in_institute = []
    authors_collaboration = dict()

    for document in authors_collection.find():
        authors_in_institute.append(document['name'])

    for document in authors_collection.find():
        cooperating_authors = []
        for article in document['articles']:
            if article['year'] != '':
                if int(article['year']) in range(decade+1, decade + 10):
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

        authors_collaboration[document['name']] = {'internal': len(cooperating_internal_authors),
                                                   'external': len(cooperating_external_authors)}

    return authors_collaboration


def most_collaborators(decade, count):
    authors_internal_dict = dict()
    authors_external_dict = dict()
    for key, value in collaborators_by_decade(decade).items():
        authors_internal_dict[key] = value['internal']
        authors_external_dict[key] = value['external']

    authors_internal_dict = sorted(authors_internal_dict.items(), key=itemgetter(1))
    authors_external_dict = sorted(authors_external_dict.items(), key=itemgetter(1))

    draw_plot(authors_internal_dict, 'Internal collaborators in ' + str(decade),
              'internal_collaborators_' + str(decade) + '.png', count)
    draw_plot(authors_external_dict, 'External collaborators in ' + str(decade),
              'external_collaborators_' + str(decade) + '.png', count)


most_collaborators(2000, 0)
