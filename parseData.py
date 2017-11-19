import re
import os
import pprint

authors_dict = dict()
DATA_DIR = './data/'
for filename in os.listdir(DATA_DIR):
    print(filename)

    publications_dict = dict()

    with open(DATA_DIR + filename) as f:
        publications = f.read().split('@')
        publications.pop(0)

        for index, publication in enumerate(publications):
            authors = ''
            searchObj = re.search(r'(author={.*})', publication)

            if searchObj:
                authors = searchObj.group()

            searchObj = re.search(r'(year={.*})', publication)
            if searchObj:
                publications_dict[index] = authors + ' ' + searchObj.group()

    authors_dict[filename[:-4]] = publications_dict

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(authors_dict)
