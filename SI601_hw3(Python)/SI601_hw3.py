# -*- coding: utf-8 -*-
import urllib2
import time
import re
import csv
from bs4 import BeautifulSoup
import json, urllib2
import xml.etree.ElementTree as ET

####################################STEP 1#################################################
#####Top 1-50
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
response1 = urllib2.urlopen('http://www.imdb.com/search/title?at=0&genres=sci_fi&sort=user_rating&start=1&title_type=feature')
html_doc1 = response1.read()
# print html_doc
soup1 = BeautifulSoup(html_doc1,"html.parser")
# soup1 = soup1.prettify()
outfile1 = open('html_doc1.html', 'w')
outfile1.writelines(soup1.encode('utf-8'))
outfile1.close()

#####Top 51-100
response51 = urllib2.urlopen('http://www.imdb.com/search/title?at=0&genres=sci_fi&sort=user_rating&start=51&title_type=feature')
html_doc51 = response51.read()
# print html_doc
soup51 = BeautifulSoup(html_doc51,"html.parser")
# soup51 = soup51.prettify()
outfile51 = open('html_doc51.html', 'w')
outfile51.writelines(soup51.encode('utf-8'))
outfile51.close()

#####Top 101-150
response101 = urllib2.urlopen('http://www.imdb.com/search/title?at=0&genres=sci_fi&sort=user_rating&start=101&title_type=feature')
html_doc101 = response101.read()
# print html_doc
soup101 = BeautifulSoup(html_doc101, "html.parser")
# soup101 = soup101.prettify()
outfile101 = open('html_doc101.html', 'w')
outfile101.writelines(soup101.encode('utf-8'))
outfile101.close()
#####Top 151-200
response151 = urllib2.urlopen('http://www.imdb.com/search/title?at=0&genres=sci_fi&sort=user_rating&start=151&title_type=feature')
html_doc151 = response151.read()
# print html_doc
soup151 = BeautifulSoup(html_doc151,"html.parser")
# soup151 = soup151.prettify()

outfile151 = open('html_doc151.html', 'w')
outfile151.writelines(soup151.encode('utf-8'))
outfile151.close()

####################################STEP 2#################################################
# soup1 = BeautifulSoup(html_doc1)
# soup1 = soup1.prettify()
rankList = list()
step2_out = open('step2_top_200_scifi_movies.tsv', 'w')
imdbidList = list()
# url = re.compile()
# print soup1.tbody
# print type(soup1)
soupList = [soup1, soup51, soup101, soup151]
for i in soupList:
	for movie in i.find("table", class_="results").find_all("tr")[1:]:
		rank = movie.find('td', class_='number').string.replace('.', '')
		link = movie.find(class_="title")
		# if link:
		url = link.a.get('href')	
		imdb_id = re.search(r'^/title/(\w*?)/', url).group(1)
		imdbidList.append(imdb_id)
		title = movie.find('td', class_='title').a.string  #return movie name
		year = link.find('span', class_='year_type').string
		# print year
		rating_area = link.find('span', class_='value')
		# print rating_area
		if rating_area:
			rating = rating_area.string
		else:
			rating = 'NA'
		# print year, rating
		# print type([rank, imdb_id, title, year, rating])
		rankList.append([rank, imdb_id, title, year, rating])
		# print rankList

step2_out.write('\t'.join(['Rank', 'IMDB ID', 'Title', 'Year', 'Rating']) + '\n')
for j in rankList:
	line = '\t'.join(list(j)) + '\n' 
	step2_out.write(line.encode('utf-8'))
step2_out.close()

####################################STEP 3#################################################
#API key: 8a8057a4392a1dc05d3e3b1754430cbb

# output3 = open('output3.txt', 'w')

# for i in imdbidList:
# 	# print i
# 	url = 'http://api.themoviedb.org/3/find/%s?api_key=8a8057a4392a1dc05d3e3b1754430cbb&external_source=imdb_id' % (i,)
# 	# # urlResponse = urllib2.urlopen('http://api.themoviedb.org/3/find/%s?api_key=8a8057a4392a1dc05d3e3b1754430cbb&external_source=imdb_id' % i)	
# 	# # output3.write(i + '\t' + readJson + '\n')
# 	urlResponse = urllib2.urlopen(url)	
# 	readJson = urlResponse.read()
# 	output3.write(i + '\t' + readJson + '\n')
# 	time.sleep(8)
# output3.close()
# 	print url
####################################STEP 4#################################################
fhand = open('step3.txt', 'rU')
themoviedbDict = dict()
count = 0
for movie in fhand:
	movie = movie.strip()
	s = movie.split('\t')
	count += 1
	movie_decode = json.loads(s[1])
	#missing values exist
	if len(movie_decode['movie_results']) > 0:
		themoviedb = movie_decode['movie_results'][0]['vote_average']
	else:
		themoviedb = 0
	themoviedbDict[s[0]] = themoviedb
fhand.close()		
# print themoviedbDict	
#IMDB ID, Title, Year, IMDB Rating, themoviedb Rating
# fhand2 = open('step2_out.tsv', 'rU')
totalList = list()
count = 0
for line in rankList:
	
	rank = line[0]
	imdb_id = line[1]
	title = line[2]
	# print title
	year = line[3]
	rating = line[4]
	
 	if rating != 0 and themoviedbDict[imdb_id] != 0:
 		count += 1
 		l = [imdb_id, title, year,rating, themoviedbDict[imdb_id]]
                totalList.append(l)
       # print len(totalList),themoviedbDict[imdb_id],imdb_id, count
 
step4_out = open('step4.csv', 'w')
writer=csv.writer(step4_out)
writer.writerow(['IMDB ID', 'Title', 'Year', 'IMDB Rating', 'themoviedb Rating'])
	
writer.writerows(totalList)

step4_out.close()
# step4_out.write('\t'.join(['Rank', 'IMDB ID', 'Title', 'Year', 'Rating']) + '\n')
# for j in rankList:
# 	line = '\t'.join(list(j)) + '\n' 
# 	step2_out.write(line.encode('utf-8'))
# step2_out.close()


	# print type(movie_decode), movie_decode['movie_results']
	# themoviedb = movie_decode['movie_results'][0]['vote_average']
	# print count, movie_decode['movie_results'][0]
# 	themoviedbDict[s[0]] = themoviedb
# print themoviedbDict







