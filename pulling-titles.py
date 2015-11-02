#!/usr/local/bin/python 

import urllib2
import csv
from bs4 import BeautifulSoup
from unidecode import unidecode

# Some globals
PAPERS = ["https://www.aeaweb.org/", \
		 "http://www.jstor.org/journal/jpoliecon", \
		 "https://www.econometricsociety.org/publications/econometrica/browse"]
AER = "/articles.php?doi=10.1257/aer."


def Souping(url):
	print "Parsing the page " + url
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	return soup

# Test run
soup = Souping(PAPERS[0] + "aer/issues.php")

previous_issues = []

for link in soup.find_all('a', href=True):
	if AER in link["href"]:
		previous_issues.append(link["href"])
	# TODO: Add JPE and Econometrica

titles = []

for issue in previous_issues:
	# TODO: Add month-year of each issue
	issue_soup = Souping(PAPERS[0] + issue)
	for link in issue_soup.find_all('a', href=True):
		if "articles.php" in link["href"]:
			try:
				text = unidecode(link.text)
			except:
				text = link.text
			titles.append(text)

for title in titles:
	print title

# TODO: Fix outputting.
# print "Writing to CSV file."
# with open('test.csv', 'w') as f:
#     a = csv.writer(f)
#     a.writerows(titles)
