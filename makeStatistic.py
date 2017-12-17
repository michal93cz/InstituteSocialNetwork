from pymongo import MongoClient
from operator import itemgetter
import matplotlib.pyplot as plt


def draw_plot(collection, title, file_name, count):
    fig = plt.figure()
    ax = fig.add_subplot(111)

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


client = MongoClient()
db = client['INS']
authors_collection = db['authors']

authors_internal_dict = dict()
authors_external_dict = dict()
for document in authors_collection.find():
    authors_internal_dict[document['name']] = len(document['internal_collaborators'])
    authors_external_dict[document['name']] = len(document['external_collaborators'])

authors_internal_dict = sorted(authors_internal_dict.items(), key=itemgetter(1))
authors_external_dict = sorted(authors_external_dict.items(), key=itemgetter(1))

draw_plot(authors_internal_dict, 'Internal collaborators', 'internal_collaborators.png', 5)
draw_plot(authors_external_dict, 'External collaborators', 'external_collaborators.png', 5)
