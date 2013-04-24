#!/usr/bin/env python
# encoding: utf-8

# get your data here
# ftp://ftp.fu-berlin.de/pub/misc/movies/database/

import re
import json
from hashlib import sha1
import codecs


# import requests
# url = "http://33.33.33.33:9200/"
# def index_item_to_es(item):
#     requests.put(url, data=item)
#     pass

#listname = "ACTOR"
listname = "ACTRESSES"


def write_a_bulk_file(items):
    with open('%s.json' % listname.lower(), 'w') as f:
        lines = '\n'.join(items)
        lines += '\n'
        f.write(lines)


def main(buffer):
    somelines = buffer.split('THE %s LIST' % listname)[1]
    somelines = somelines[50:]
    splittedlist = somelines.split('\n\n')

    items = []

    for item in splittedlist[:50000]:
        item = [x.split('\t') for x in item.split('\n\t\t\t')]
        item = item[0]
        name = item[0]

        indexit = True

        try:
            role = re.search(r"\[.*?\]", item[-1])
            role = role.group()[1:-1]
        except:
            role = ""
            indexit = False
        try:
            year = re.search(r"\(\d*\)", item[-1])
            year = year.group()[1:-1]
        except:
            year = ""
            indexit = False
        title = item[-1].split(' (')[0]

        if title and name:
            indexit = True
        else:
            indexit = False

        newitem = {
            'name': name.decode('latin1'),
            'role': role.decode('latin1'),
            'year': year,
            'title': title.decode('latin1')
        }

        if indexit is True:

            items.append(json.dumps({"index": {"_type": "actors", "_id": sha1(name+title+year).hexdigest() }}))
            items.append(json.dumps(newitem))

            # get all movies by actor
            for movie in item[1:]:
                try:
                    role = re.search(r"\[.*?\]", movie)
                    role = role.group()[1:-1]
                except:
                    role = ""
                try:
                    year = re.search(r"\(\d*\)", item[-1])
                    year = year.group()[1:-1]
                except:
                    year = ""
                title = movie.split(' (')[0]

                newitem = {
                    'name': name.decode('latin1'),
                    'role': role.decode('latin1'),
                    'year': year,
                    'title': title.decode('latin1')
                }
                items.append(json.dumps({"index": {"_type": "actors", "_id": sha1(name+title+year).hexdigest() }}))
                items.append(json.dumps(newitem))

    write_a_bulk_file(items)


if __name__ == '__main__':
    with open('%s.list' % listname.lower()) as f:
        buffer = f.read()
    main(buffer)