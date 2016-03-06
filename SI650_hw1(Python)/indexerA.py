#os.listdir(path)
import sys, getopt
import json
import os
import nltk
from nltk.stem import *
from nltk.stem.porter import *
# from nltk import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
import string
import xml.etree.ElementTree as ET
import collections
import utils
#--------------------------------------A1----------------------------#

argList = sys.argv  #a list of args
# print argList,type(argList)
stemmer = SnowballStemmer("english")
doc = argList[1] #find out the target file
# print doc, 'hahahaha'
dirs = os.listdir(doc) #get all the documents
# print dirs, len(dirs)

docDict = dict() #create a dict to story  key: docId value: list containing all words of that document
# docId = 0
# docIdList = list()
allWordList = list()
# def index(str):

for document in dirs:  #loop every document
	lenDict = dict()
	docList = list()  #create a list to store all strings in this document
	docName = document.strip('\n')
	docPath = '/home/650/resources/Homework1/cranfieldDocs'
	tree = ET.parse(docPath + '/' + docName)
	root = tree.getroot()
	# docId += 1
	docId = root.find('DOCNO').text.strip()
	# if docId == '820':
	# 	print docId, type(docId)
		
	for element in root.itertext():  #evey root in XML file
		# print element,'thsi is element'
		token_list = nltk.word_tokenize(element)  #tokenize
	
		for token in token_list:
			
			tokenStem = stemmer.stem(token)  #stemming

			if tokenStem != '':
				allWordList.append(tokenStem)
			
			docList.append(tokenStem)
			docPuncList = list()
			docPuncList = [''.join(c for c in s if c not in string.punctuation) for s in docList]			
			docPuncList = [s for s in docPuncList if s]  #exclude empty string
	docDict[docId] = docPuncList		
# print docDict,'this is docDoci'
# print docDict['820']

#--------------------------------------A2----------------------------#
# pos = list()  #[docId, position]
# wordList = list()  #[word, [posList]]
invIndexList = list() #[wordList]
allWordListLower = list()

for word in allWordList:
	word = word.lower()
	allWordListLower.append(word)
# print set(allWordListLower)
# set(allWordListLower)		
for word in set(allWordListLower):
	# print word, 
	posList = list() #  [[docId, position], [docId, position]]
	for i in docDict:
		# print i,'this is i'
		position = 0
		
		for w in docDict[i]:

			if w.lower() == word:
				pos = [i, position]
				# print pos, 'this is pos'
				posList.append(pos)
				posList.sort()
				# print posList,'this is posList'
			position += 1

	wordList = [word, posList]
	# print wordList,'this is wordList'
	# if wordList[0] == 'plastic':
	# 	print wordList[0], 'hahahahahaha', '\n', wordList[1]
	# print 'hahahah'	
	# if wordList[0] == 'buckling':
	# 	print 'Hey'
	# 	print wordList[0], 'hahahahahaha', '\n', wordList[1]	
	invIndexList.append(wordList)
	invIndexList.sort()
print invIndexList
# for i in invIndexList:
# 	if i[0] == "plastic":
# 		print i[1]
with open('indexA.json', 'w') as outfile:
    json.dump(invIndexList, outfile)













