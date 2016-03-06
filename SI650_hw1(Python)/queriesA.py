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
import re
from collections import OrderedDict

#--------------------------------------A4------------------------------------#
json_data = open('indexA.json', 'rU')
dataList = json.load(json_data)
lenDict = dict()


for item in dataList:
	wordPos = item[1]
	for pos in wordPos:
		if pos[0] not in lenDict:
			lenDict[pos[0]] = 1
		else:
			lenDict[pos[0]] = lenDict[pos[0]] + 1 

#--------------------------------------A5------------------------------------#
argList = sys.argv  #a list of args
# print argList,type(argList)
stemmer = SnowballStemmer("english")
doc = argList[1] #find out the target file
docPath = '/home/650/resources/Homework1/'
readFile = open(doc, 'rU')
# s = '"plastic buckling"'
queryAnd = re.compile(r'(.*)\sAND\s(.*)')
queryLink = re.compile(r'"(.*?)"')
queryOr = re.compile(r'(.*)\s(.*)')
# s = '"plastic" AND "shear"'
# s = 'plastic'

def intersect(l1, l2):
	l1.sort()
	l2.sort()
	rankDict = dict()
	sort_result = list()
	intersect_result = list()
	i = 0
	j = 0
	while (i < len(l1) and j < len(l2)):
		if l1[i][0] == l2[j][0]:
			intersect_result.append(l1[i])  # append [docid, pos]
			i += 1
			j += 1
		elif l1[i][0] > l2[j][0]:	
			j += 1
		else:
			i += 1
	intersect_result.sort()		
	return intersect_result

def multi_intersect(l):
	# multi_intersect_result = list()
	# print 'this is start of l',l, len(l),'this is l, jinxingchi'
	multi_intersect_result = l[0]
	rankDict = dict()
	sort_result = list()
	for i in range(1, len(l)):
		# i = i + 1
		multi_intersect_result = intersect(multi_intersect_result, l[i])
	
	for key in multi_intersect_result:
		if key[0] not in rankDict:
			# print key[0], 'this is a key ling'
			rankDict[key[0]] = 1
		else:
			rankDict[key[0]] = rankDict[key[0]] + 1

	for key in rankDict:
		rankDict[key] = [rankDict[key],lenDict[key]]
	for key in sorted(rankDict.items(),key = lambda item:(-item[1][0],item[1][1])):	
		sort_result.append(key)

	# for p in OrderedDict(sorted(rankDict.items(), key=lambda t: -t[1] )):
		# sort_result.append(p) 
	# print rankDict['1119'], rankDict['1121'],rankDict['820'], 'this is rankDict'	
	# print rankDict, 'this is rankDict '
	# print OrderedDict(sorted(rankDict.items(), key=lambda t: (-t[1], lenDict[t[0]] ) )), 'this is a sorted multi_intersect'
	return sort_result	

def union(l1, l2): ##This function is for finding the union of two list
	l1.sort()
	l2.sort()
	rankDict = dict()
	sort_result = list()
	unin_result = list()
	# i = 0
	# j = 0
	unin_result = l1 + l2
	# for pos in unin_result:
	# 	unin_result.append(pos[0])
	# print unin_result, 'this is unin_result'
	return unin_result

def multi_union(l):      ##This function is for finding the union of multiple list [docid1,docid2...]
	# print l,'this is a l',len(l)
	multi_union_result = l[0]
	posList = list()
	# print type(multi_union_result),'hello'
	rankDict = dict()
	sort_result = list()
	for i in range(1, len(l)):
		# i = i + 1
		multi_union_result = union(multi_union_result, l[i])
	# print multi_union_result,'this is multi_union_result', len(multi_union_result)	
	# for pos in multi_union_result:
	# 	posList.append(pos[0])
	for pair in multi_union_result:	 
		# print pair, 'this is items'
		# for pair in item: #item ['o',3]	

	# # print posList, 'this is posList', type(list(posList))
	# 	for key in multi_union_result:
	# 		print 'start of  key',key, 'this is key'
	# 		# print key[0], 'this is key ling'
	# 		# for item in 
		if pair[0] not in rankDict:
			# print 'staris pair[0]',pair[0], type(pair[0]),'this is pair[0]'
			rankDict[pair[0]] = 1
		else:
			rankDict[pair[0]] = rankDict[pair[0]] + 1
	# print rankDict,'this is rankDict shagougougou shagougougou'		
	for key in rankDict:
		# print key, 'this is key'
		rankDict[key] = [rankDict[key],lenDict[key]]			

	# print rankDict,'this is rankDict shagougougou shagougougou'
	for key in sorted(rankDict.items(),key = lambda item:(-item[1][0],item[1][1])):	
		sort_result.append(key)

	# print rankDict,'this is multi_union rankDict'
	return sort_result	

def findIndex(s):   ##This fuction is for finding index of a single word
	posList = list()
	for i in dataList:
		word = i[0]
		if word == stemmer.stem(s.lower()):
			# print word, 'this is word in findIndex'
			position = i[1]
	
	return position    #[docid,docid...]
	# return list(set(idList))	

def findMultiIndex(l1, l2):  ##This function is for finding index of "plastic shear" (only two words)
	# print type(l1), type(l2),l1, l2, 'this is si and s2'
	positionS1 = l1
	positionS2 = l2
	resultList = list()
	docid_resultList  =list()
	j = 0
	k = 0
	if positionS1 != None and positionS2 != None:	
		while (j < len(positionS1) and k < len(positionS2)):
			if positionS1[j][0] == positionS2[k][0]: #docId equal
				positionS2_i = positionS2[k][1] - 1
					
				if positionS1[j][1] == positionS2_i:
						# if l1[i] == l2[j]:
					resultList.append(positionS2[k])
					
					j += 1
					k += 1
				elif positionS1[j][1] > positionS2_i:	
							# p2 += 1
					k += 1
				else:
							# p1 += 1
					j += 1

			elif positionS1[j][0] > positionS2[k][0]:
				k += 1
			elif positionS1[j][0] < positionS2[k][0]:	
				j += 1
	# print resultList, 'this is findMultiIndex resources'  [[u'1013', 109], [u'1067', 26], [u'1119', 162], [u'
	if len(resultList) ==0:
		# return []
		# print '000', 'this is 000'
		return ["000"]
	for doc in resultList:
		docid_resultList.append(doc)
	# print docid_resultList,'this is findMultiIndex resources' 
	return docid_resultList				

def findAllIndex(l):   ##This function is for finding word like "plastic buckling shear cat"
	# wordList = list()
	# print l, 'this is l'
	# for i in dataList:
	# 	word = i[0]
	# 	posList = i[1]
	findAllIndexList = list()
	findAllIndexList = l[0]
	# print l[0], 'this is l0'
	pairIndexList = list()

	for i in range(1, len(l)):
		# print findAllIndexList, 'this is findAllIndexList'
		if findAllIndexList[0] != "000":
			# print 'start o fli' ,l[i], 'this is l[i]'
		# i = i + 1
			findAllIndexList = findMultiIndex(findAllIndexList, l[i])
			# pairIndexList.append(findAllIndexList)

		else: 
			findAllIndexList = []
			
	# print 'start of findAllIndexList',multi_intersect(pairIndexList), 'this is findMultiIndex'	
	return findAllIndexList
	# return docid_resultList				

queryList = list()
for line in readFile:
	line = line.strip()
	# line.lower()
	# print type(line)
	# print line
	s = line
	# s = 'plastic plastic'
	# s = 'plastic'
	# s = '"the theory of"'
	# s = '"plastic buckling"'
	# s = 'plastic AND "stress buckling" AND shear AND buckling AND the AND "theory" AND "a" '
	if queryAnd.search(s) != None:
		andList = list()
		paraList_and = list()
		# print 'inside_1'
		andGrp = queryAnd.search(s).group(1).split('AND') #return a list 
		lastGrp = queryAnd.search(s).group(2)  #return the last item
		andGrp.append(lastGrp)   #the whole AND list
		for x in andGrp: 
			print x   
			x = x.strip()
			andList.append(x.lower()) 

		# print paraList_and, 'this is paraList_and', len(paraList_and)

		if queryLink.search(s) == None:
			for i in andList:
				# print i , 'this is i'
				paraList_and.append(findIndex(stemmer.stem(i)))

			print 'Query: ',s,'\n', 'Matching documents:'  
			# print multi_intersect(paraList_and), 'this is multi_intersect'
			for i in multi_intersect(paraList_and):
				print i[0]
		# print multi_intersect(paraList_and)	, 'this is teh nultisection'
			# print Grp
			#now see if there are "" among grpList
		if queryLink.search(s) != None:
			otherList =list()
			paraList =list()
			# print 'inside_2'
			quoList = queryLink.findall(s)
			# print quoList,'this is quoList,shagougougou'
			for i in quoList:
				allword = list()
				word = i.split(' ')  #a list [dog,cat]
				#print word,'this is word~~~~'
				for j in word:
					for d in dataList:
						word_dataList = d[0]
						# resultList = list()
						# docid_resultList  =list()
						if word_dataList == stemmer.stem(j.lower()):
							# print 'shagougougou',d[1],'end of j'
							d[1].sort()
							allword.append(d[1])
				paraList.append(findAllIndex(allword))			

			for other in andList:
				# print queryLink.findall(other), 'this is queryLink.findall(other)'
				if len(queryLink.findall(other))==0:
				#print other, type(other),'this is other,shagougougou'
				# if queryLink.findall(other)[0] not in quoList:
					# print queryLink.findall(other), 'this is queryLink.findall(other)'
					#print quoList[0], quoList[1],'these are quotes'
					# print other, 'this is other not in quoList'
					paraList.append(findIndex(stemmer.stem(other.lower())))
			
			print 'Query: ',s, '\n','Matching documents:'
			# print multi_intersect(paraList), 'this is multi_intersect'
			if len(multi_intersect(paraList)) != 0:
				for i in multi_intersect(paraList):  
					print i[0] 
					# print i[0], 'shagougougou'
			else:
				print "no Matching found"

	##-----------------------end of AND------start of OR + ""---------------------#
	elif queryLink.search(s) != None:
		exclude_quo = re.sub(r'"(.*?)"', '',s.lower())
		# print 'this is a quote'
		otherList = exclude_quo.split(' ')   #word with no quote
		# print otherList, 'this is other list', len(otherList)
		paraList = list()
		# allOrList = list()
		if otherList != ['']:
			# print 'len not zero'
			# nonSpaceList = list()
			for i in otherList:
				# print i,'this is in in otherList'
				if i != '':
					# print i, 'this is i'
					paraList.append(findIndex(stemmer.stem(i.lower())))
				# print paraList, 'this is paraList in the other list'
				# if i == ' ':
				# 	print 'paraList not found'
				# 	break
		# paraList =list()
		# print 'inside_2Link query'
		quoList = queryLink.findall(s)
		# print quoList, 'this is quoList'
#----------------------------------
		for i in quoList:
			# print i, 'this is i in quoteList'
			allword = list()
			word = i.split(' ')  #a list [dog,cat]
			# print word,'this is word~~~~'
			for j in word:
				# print j,'this is j in word'
				for d in dataList:

					word_dataList = d[0]
						# resultList = list()
						# docid_resultList  =list()
					if word_dataList == stemmer.stem(j.lower()):
						# print 'shagougougou',d[0],'end of j'
						d[1].sort()
						allword.append(d[1])
						# print len(allword), 'this is length of allword'
			# print findAllIndex(allword)	, 'this is allword'		
			paraList.append(findAllIndex(allword))

# ---------------------------------
		
		print  'Query: ',s, '\n','Matching documents:'
		# print multi_union(paraList),'this is multi_union'
		if paraList[0] == ['000']:
			print 'document not found'
		else:
				
			for i in multi_union(paraList):
				# print paraList, 'this is paraList'
				# print multi_union(paraList)
				print i[0]

	##---------------------------start of or, no ""-------------------#
	elif queryLink.search(s) == None:
		# print 'no quote'
		wordList = s.split(' ')
		# print wordList,'this is wordList'
		spaceList = list()

		for i in wordList:
			# print findIndex(stemmer.stem(i)), 'index'

			spaceList.append(findIndex(stemmer.stem(i.lower())))
		# print 'start of spaceList',spaceList,len(spaceList), 'end of spaceList'
		# print findIndex(stemmer.stem(i.lower())),'this is findIndex,,,,,,'
		print 'Query: ',s, '\n',  'Matching documents:'
		# print multi_union(spaceList), 'this is multi_union(spaceList)'
		for i in multi_union(spaceList):
			print i[0]			# len(multi_union(spaceList)),'the end i'
			# print i[0]  , 'the end'


				
	








