import urllib2
import pprint
import csv
from bs4 import BeautifulSoup
from unidecode import unidecode

def pull_AER_abstracts():

	journal = "AER"

	print "Parsing AER articles list."
	
	def Souping(url):
		response = urllib2.urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')
		return soup

	soup = Souping("https://www.aeaweb.org/aer/issues.php")

	print "Grabbing previous issues."

	def GrabPrevIssues(soup):
		previous_issues = []
		for link in soup.find_all('a', href=True):
			if "/articles.php?doi=10.1257/aer." in link["href"]:
				previous_issues.append(link["href"])	
		return previous_issues

	all_issues = GrabPrevIssues(soup)

	print "Preparing to clean text."

	def CleanText(element):
		try:
			string = unidecode(element.text)
		except:
			string = element.text
		return string

	print "Preparing to create data."

	def CreateData(titles, date_of_issue, text_string, journal):
		if text_string != "":	
			titles.append({'date': date_of_issue,
							'title': text_string,
							'journal': "AER"})

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

	print "Grabbing previous issues' article abstracts."

	def GrabArticleLinks(all_issues):
		article_links = []
		for issue in all_issues:
			issue_soup = Souping("https://www.aeaweb.org/" + issue)
			for link in issue_soup.find_all('a', href=True):
				if "articles.php" in link["href"]:
					article_links.append(link["href"])	
		return article_links

	all_article_links = GrabArticleLinks(all_issues)

	def GrabTitleAbstracts(all_article_links, journal):
		abstracts = []
		for article_link in all_article_links:
			article_soup = Souping("https://www.aeaweb.org/" + article_link)
			issue_date = article_soup.find_all("h1")[0].text[-15:]
			for para in article_soup.find_all("div", "sub_head_info"):
				if "(JEL" in para:
					text = CleanText(para)
					CreateData(titles, issue_date, text, journal)
		return abstracts

	all_abstracts = GrabTitleAbstracts(all_issues, journal)

	print "Writing to CSV file."

	def OutputtingCSV(abstracts, journal):
		keys = abstracts[0].keys()
		with open("AER_abstracts_simple.csv", 'wb') as f:
			a = csv.DictWriter(f, keys)
			a.writeheader()
			a.writerows(abstracts)

	OutputtingCSV(all_abstracts, journal)

pull_AER_abstracts()
