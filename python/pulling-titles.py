#!/usr/local/bin/python 

import urllib2
import pprint
import csv
from bs4 import BeautifulSoup
from unidecode import unidecode

# Some globals
PAPERS = [{"name": "AER", "top": "https://www.aeaweb.org/", "issues": "/articles.php?doi=10.1257/aer.", "tail": "aer/issues.php"},
		 {"name": "JPE", "top": "http://www.jstor.org/journal/jpoliecon", "issues": "" , "tail": ""},
		 {"name": "Econometrica", "top": "https://www.econometricsociety.org/", "issues": "/publications/econometrica/issue/", "tail": "publications/econometrica/browse"}]


def Souping(url):
	print "Parsing " + url + "."
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	return soup


def GetOldIssues(journal_soup, journal):
	print "Grabbing previous issues."
	previous_issues = []

	for link in journal_soup.find_all('a', href=True):
		if journal['issues'] in link["href"]:
			previous_issues.append(link["href"])	
		# TODO: Add JPE and Econometrica

	return previous_issues


def CleanText(element):
	try:
		string = unidecode(element.text)
	except:
		string = element.text
	return string


def CreateData(titles, date_of_issue, text_string, journal):
	if text_string != "":	
		titles.append({'date': date_of_issue,
				'title': text_string,
				'journal': journal['name']})


def GetIssueTitles(previous_issues, journal):
	print "Now grabbing previous issues' article titles."
	titles = []

	for issue in previous_issues:
		issue_soup = Souping(journal['top'] + issue)

		if journal['name'] == "AER":
			issue_date = issue_soup.find_all("h1")[0].text[-15:]

			for link in issue_soup.find_all('a', href=True):
				if "articles.php" in link["href"]:
					text = CleanText(link)
					CreateData(titles, issue_date, text, journal)


		if journal['name'] == "Econometrica":
			issue_date = issue_soup.find_all("h1")[0].text
			print issue_date

			for title in issue_soup.find_all(class_="featured_paper_content"):
				# print title.find("strong").text
				text = CleanText(title.find("strong"))
				CreateData(titles, issue_date, text, journal)
				# print text	



	return titles

def OutputtingCSV(titles, journal):
	print "Writing to CSV file."

	keys = titles[0].keys()

	with open('data/titles_' + journal['name'] + '.csv', 'wb') as f:
	    a = csv.DictWriter(f, keys)
	    a.writeheader()
	    a.writerows(titles)


soup = Souping(PAPERS[1]['top'] + PAPERS[1]['tail'])
old_issues = GetOldIssues(soup, PAPERS[1])
all_titles = GetIssueTitles(old_issues, PAPERS[1])
OutputtingCSV(all_titles, PAPERS[1])

# Full run
# for paper in PAPERS:	

# 	soup = Souping(paper['top'] + paper['tail'])
# 	old_issues = GetOldIssues(soup, paper)
# 	all_titles = GetIssueTitles(old_issues, paper)

# 	OutputtingCSV(all_titles, paper)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(all_titles)



