#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from facebook import *
import humanRandom

def main(username,password):
    """ Opens FacebookClient and posts random status """
    fb = FacebookClient(username,password)
    humanRandom.searchEngineWaitTime()
    print("brithdays...")
    fb.happy_birthdays()
    fb.destroy()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

