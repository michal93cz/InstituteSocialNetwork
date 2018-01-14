from pprint import pprint

from pymongo import MongoClient
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np

client = MongoClient()
db = client['INS']
authors_collection = db['authors']

authors_in_institute = []
for document in authors_collection.find():
    authors_in_institute.append(document['name'])


def draw_plot(collection, title, file_name, count, pair=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if count != 0:
        collection = collection[-count:]

    authors_labels, ys, xs = [], [], []
    index = 0
    for authors, x in collection:
        ys.append(index)
        if pair:
            authors_labels.append(authors[0] + ' / ' + authors[1])
        else:
            authors_labels.append(authors)
        xs.append(x)
        index += 1

    ax.barh(ys, xs)
    plt.title(title)
    plt.yticks(ys, authors_labels)
    plt.tight_layout()
    fig.savefig(file_name)


def collaborators_by_decade(decade):
    authors_collaboration = dict()

    for document in authors_collection.find():
        cooperating_authors = []
        for article in document['articles']:
            if article['year'] != '':
                if int(article['year']) in range(decade+1, decade + 10):
                    for author in article['authors']:
                        cooperating_authors.append(author.lstrip())

        cooperating_authors = np.unique(cooperating_authors).tolist()

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


def pairs_by_decade(decade):
    authors_pairs_collaboration = dict()

    for document in authors_collection.find():
        cooperating_authors = []
        for article in document['articles']:
            if article['year'] != '':
                if int(article['year']) in range(decade+1, decade + 10):
                    for author in article['authors']:
                        cooperating_authors.append(author.lstrip())

        unique, counts = np.unique(cooperating_authors, return_counts=True)
        cooperating_authors = dict(zip(unique, counts))

        for key, val in cooperating_authors.items():
            if key in authors_in_institute:
                authors_pairs_collaboration[(document['name'], key)] = val

    keys_list = set(tuple(sorted(t)) for t in authors_pairs_collaboration)

    final_dict = dict()
    for (key1, key2) in keys_list:
        if (key1, key2) in authors_pairs_collaboration.keys():
            final_dict[(key1, key2)] = authors_pairs_collaboration[(key1, key2)]
        else:
            final_dict[(key1, key2)] = authors_pairs_collaboration[(key2, key1)]

    return final_dict


def internal_collaborators(decade, count, dir_to):
    authors_internal_dict = dict()

    for key, value in collaborators_by_decade(decade).items():
        authors_internal_dict[key] = value['internal']

    authors_internal_dict = sorted(authors_internal_dict.items(), key=itemgetter(1))

    draw_plot(authors_internal_dict, 'Internal collaborators in ' + str(decade),
              dir_to + 'internal_collaborators_' + str(decade) + '.png', count)


def external_collaborators(decade, count, dir_to):
    authors_external_dict = dict()

    for key, value in collaborators_by_decade(decade).items():
        authors_external_dict[key] = value['external']

    authors_external_dict = sorted(authors_external_dict.items(), key=itemgetter(1))

    draw_plot(authors_external_dict, 'External collaborators in ' + str(decade),
              dir_to + 'external_collaborators_' + str(decade) + '.png', count)


def internal_pairs_collaborators(decade, count, dir_to):
    authors_internal_pairs_dict = pairs_by_decade(decade)
    authors_internal_pairs_dict = sorted(authors_internal_pairs_dict.items(), key=itemgetter(1))

    draw_plot(authors_internal_pairs_dict, 'Internal collaborators pairs in ' + str(decade),
              dir_to + 'internal_pairs_collaborators_' + str(decade) + '.png', count, True)


def most_collaborators(decade, count, dir_to):
    internal_collaborators(decade, count, dir_to)
    external_collaborators(decade, count, dir_to)
    internal_pairs_collaborators(decade, count, dir_to)


most_collaborators(1980, 10, './')
