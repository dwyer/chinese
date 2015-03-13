#!/usr/bin/env python

# -*- encoding: utf-8 -*-

import os
import re
import sqlite3
import sys

if len(sys.argv) != 3:
    print >>sys.stderr, 'usage: %s INPUT_FILE OUTPUT_FILE' % sys.argv[0]
    exit(1)

text_file = sys.argv[1]
data_file = sys.argv[2]

if os.path.exists(data_file):
    os.remove(data_file)

connection = sqlite3.connect(data_file)
cursor = connection.cursor()
cursor.execute('CREATE TABLE words (traditional, simplified, pinyin, english)')

regex = re.compile(r'^([^\s]*) ([^\s]*) \[(.*)\] /(.*)/$')
with open(text_file) as f:
    for line in f:
        if line.startswith('#'):
            continue
        vals = [x.decode('utf-8') for x in regex.match(line.strip()).groups()]
        cursor.execute('INSERT INTO words VALUES (?, ?, ?, ?)', vals)
connection.commit()
