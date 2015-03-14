#!/usr/bin/env python

# -*- encoding: utf-8 -*-

import csv
import os
import re
import sqlite3
import sys

if len(sys.argv) != 4:
    print >>sys.stderr, 'usage: %s CEDICT_TXT TOCFL_CSV OUTPUT_DB' % sys.argv[0]
    exit(1)

cedict_file = sys.argv[1]
tocfl_file = sys.argv[2]
data_file = sys.argv[3]

if os.path.exists(data_file):
    os.remove(data_file)

connection = sqlite3.connect(data_file)
cursor = connection.cursor()
cursor.execute('CREATE TABLE cedict (traditional, simplified, pinyin, english)')
cursor.execute('CREATE TABLE tocfl (level, traditional, pinyin)')

def decode_all(lst):
    return [x.decode('utf-8') if isinstance(x, basestring) else x for x in lst]

regex = re.compile(r'^([^\s]*) ([^\s]*) \[(.*)\] /(.*)/$')
with open(cedict_file) as f:
    for line in f:
        if line.startswith('#'):
            continue
        cursor.execute('INSERT INTO cedict VALUES (?, ?, ?, ?)',
                       decode_all(regex.match(line.strip()).groups()))

with open(tocfl_file) as f:
    reader = csv.reader(f)
    reader.next() # skip header
    for level, traditional, pinyin in reader:
        cursor.execute('INSERT INTO tocfl VALUES (?, ?, ?)',
                       decode_all([int(level), traditional, pinyin]))

connection.commit()
