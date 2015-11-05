#!/usr/local/bin/python 

import urllib2
import pprint
import csv
from bs4 import BeautifulSoup
from unidecode import unidecode


journal = "AER"

def Souping(url):
	print "Now parsing " + url + "."
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	return soup

mainSoup = Souping("https://www.aeaweb.org/aer/issues.php")

def GrabPrevIssues(soup):
	print "Grabbing previous issues."
	previous_issues = []
	for link in soup.find_all('a', href=True):
		if "/articles.php?doi=10.1257/aer." in link["href"]:
			previous_issues.append(link["href"])	
	return previous_issues

all_issues = GrabPrevIssues(mainSoup)

def CleanText(element):
	print "Preparing to clean text."
	try:
		string = unidecode(element.text)
	except:
		string = element.text
	return string

def CreateData(dataset, date_of_issue, title, abstract_text, journal):
	print "Preparing to create data."
	if title != "":	
		dataset.append({'date': date_of_issue,
						'title': title,
						'abstract': abstract_text,
						'journal': journal })

# print "Grabbing previous issues' article titles."

# def GrabIssueTitles(all_issues, journal):	
# 	titles = []
# 	for issue in all_issues:
# 		issue_soup = Souping("https://www.aeaweb.org/" + issue)
# 		issue_date = issue_soup.find_all("h1")[0].text[-15:]
# 		for link in issue_soup.find_all('a', href=True):
# 			if "articles.php" in link["href"]:
# 				text = CleanText(link)
# 				CreateData(titles, issue_date, text, journal)
# 	return titles

# all_titles = GrabIssueTitles(all_issues, journal)

def GrabArticleLinks(all_issues):
	print "Grabbing previous issues' article abstracts."
	article_links = []
	for issue in all_issues:
		issue_soup = Souping("https://www.aeaweb.org/" + issue)
		for link in issue_soup.find_all('a', href=True):
			if "articles.php" in link["href"]:
				article_links.append(link["href"])	
	return article_links

all_article_links = GrabArticleLinks(all_issues[2:3])

def GrabTitleAbstracts(all_article_links, journal):
	abstracts = []

	# Looping over 
	for article in all_article_links:

		try:
			article_soup = Souping("https://www.aeaweb.org/" + article)

			# Date
			issue_date = article_soup.find_all("h1")[0].text[-15:]

			# Title
			if len(article_soup.find_all("h2")) != 0: 
				title = article_soup.find_all("h2")[0].text
			else:
				title = ""

			# Abstract
			for para in article_soup.find_all("div", "sub_head_info"):
				if "(JEL" in para.text:
					abstract_text = CleanText(para)
					CreateData(abstracts, issue_date, title, abstract_text, journal)

		except urllib2.HTTPError, e:
			print "Oh no - an error of type " + str(e)
			pass

	return abstracts

all_abstracts = GrabTitleAbstracts(all_article_links, journal)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(all_abstracts)

print "Writing to CSV file."

def OutputtingCSV(abstracts, journal):
	keys = abstracts[0].keys()
	with open("../data/AER_abstracts_simple.csv", 'wb') as f:
		a = csv.DictWriter(f, keys)
		a.writeheader()
		a.writerows(abstracts)

OutputtingCSV(all_abstracts, journal)

