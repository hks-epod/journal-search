#!/usr/local/bin/python 

import urllib2
import csv
from bs4 import BeautifulSoup

# Some globals
PAPERS = ["https://www.aeaweb.org/aer/issues.php", \
		 "http://www.jstor.org/journal/jpoliecon", \
		 "https://www.econometricsociety.org/publications/econometrica/browse"]


def getTitles(url):
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	return soup


# Test run
soup = getTitles(PAPERS[0])

print soup