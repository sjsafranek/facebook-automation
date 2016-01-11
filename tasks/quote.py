#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import csv
import random
from facebook import *
import humanRandom
import manager

def get_quotes(file):
    data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f, delimiter = "\t")
        for row in reader:
            data.append(row)
    return data

def main(username,password):
    """ Opens FacebookClient and posts random quote """
    quotes = get_quotes(os.path.join("tasks","data","quotes.csv"))
    c = random.randint(0,len(quotes)-1)
    quote = quotes[c]['QUOTE']
    username, password = manager.session()
    humanRandom.searchEngineWaitTime()
    print("found some inspirational shit:",quote)
    fb.post(quote)
    fb.destroy()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

