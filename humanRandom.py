#!/usr/bin/env python
"""
This file defines functions that apply wait times to our automated searches.
This is intended to simulate human like behaviors on the web.
"""

import time
from random import random
from random import uniform
from random import randint


__author__ = "Anthony Lazzaro, and Stefan Safranek"
__copyright__ = "Copyright 2015, Anti-Search Project"
__credits__ = ["Anthony Lazzaro", "Stefan Safranek"]

__license__ = "The MIT License (MIT)"
__version__ = "0.0.1"
__maintainer__ = "Anthony Lazzaro"
__email__ = "skynab@gmail.com"
__status__ = "Development"

# All of these can also be accomplished using a Gaussian curve.
# Re-coding them using proper mu and sigma values might be useful.



def pageWaitTime():
	""" 
	This is a probability distribution of someone's page view time history.
	This determines the wait time at each page to simulate reading.
	"""

	prob = random()
	if (prob <= 0.564):
		time.sleep( uniform(1, 10) ) #In Seconds
	elif(prob <= 0.650):
		time.sleep( uniform(11, 30) )
	elif(prob <= 0.727):
		time.sleep( uniform(31, 60) )
	elif(prob <= 0.823):
		time.sleep( uniform(61, 180) )
	elif(prob <= 0.906):
		time.sleep( uniform(181, 600) )
	elif(prob <= 0.970):
		time.sleep( uniform(601, 1800) )
	elif(prob <= 1.000):
		time.sleep( uniform(1801, 3600) )

	return

def searchEngineWaitTime():
	""" 
	This is a probability distribution of the time spent choosing a search result.
	This determines how long the user takes to navigate after searching.
	RETURNS: The probability so that 
	"""
	prob = random()

	if (prob <= 0.33):
		time.sleep( uniform(1, 4) ) #In Seconds
	elif(prob <= 0.66):
		time.sleep( uniform(5, 7) )
	elif(prob <= 0.95):
		time.sleep( uniform(8, 15) )
	elif(prob <= 1.00):
		time.sleep( uniform(16, 35) )

	return prob

def searchEngineChoice(numberOfChoices, prob = -1):
	""" 
	This is a probability distribution for how far down in the search results to pick.
	This determines which item in a list of search results to choose.
	"""

	# If no prob argument was passed make a random one.
	if( prob == -1 ): 
		prob = random()

	# If possible the link chosen should be correlated to the random time value
	# I.e. If the user waits a long time, choose a link farther down the list. 
	if (prob <= 0.33):
		return randint(0, 2)
	elif(prob <= 0.66):
		return randint(2, 5)
	elif(prob <= 0.95):
		return randint(5, numberOfChoices - 1)
	elif(prob <= 1.00):
		return randint(0, numberOfChoices - 1)



def pageDepth():
	""" 
	This is a probability distribution of the average links clicked in a website.
	This determines how far to crawl before opening another tab or going back to search.
	"""
	prob = random()

	if (prob <= 0.33):
		return randint(0, 2)
	elif(prob <= 0.66):
		return randint(2, 3)
	elif(prob <= 1.00):
		return randint(3, 5)



