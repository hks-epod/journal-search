#!/usr/local/bin/python 

import urllib2
import csv
from bs4 import BeautifulSoup

# Some globals
PAPERS = ["https://www.aeaweb.org/aer/issues.php", \
		 "http://www.jstor.org/journal/jpoliecon", \
		 "https://www.econometricsociety.org/publications/econometrica/browse"]
AER = "/articles.php?doi=10.1257/aer."


def Souping(url):
	print "Parsing the top-level page..."
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	return soup

# Test run
soup = Souping(PAPERS[0])

for link in soup.find_all('a'):
	print link
	if AER in link:
		print link


# print soup