#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from facebook import *
import humanRandom

def main(username,password):
    """ Opens FacebookClient and posts random status """
    username, password = manager.session()
    fb = FacebookClient(username,password)
    humanRandom.searchEngineWaitTime()
    print("doing something fun...")
    fb.set_status()
    fb.destroy()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

