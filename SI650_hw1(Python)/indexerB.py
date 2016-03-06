import sys, getopt
import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
# from lucene import QueryParser, IndexSearcher, IndexReader, StandardAnalyzer,TermPositionVector, SimpleFSDirectory, File, MoreLikeThis, VERSION, initVM, Version

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
#--------------------------------------B1------------------------------------#

if __name__ == '__main__':
	# INDEX_DIR = '/home/650/resources/Homework1/cranfieldDocs'
	lucene.initVM()
	# print "lucene version is:", lucene.VERSION

	argList = sys.argv# get the arguments
	# print argList[1]
	targetDoc = argList[1]
	dirs = os.listdir(targetDoc) #get all the documents
	# print dirs
	##set up directroy
	indexDir = SimpleFSDirectory(File("Index"))
	analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
	##get IndexWriterConfig
	writerConfig = IndexWriterConfig(Version.LUCENE_4_10_1, StandardAnalyzer())
	#get the index storage
	# store = lucene.SimpleFSDirectory(lucene.File(INDEX_DIR))
	##get the writer
	writer = IndexWriter(indexDir, writerConfig)

	
	#--------------------------------------B2------------------------------------#
	# print "%d docs in index" % writer.numDocs()
	# print "Reading lines from sys.stdin..."
	for document in dirs:  #loop every document
		# docList = list()  #create a list to store all strings in this document
		docName = document.strip('\n')
		docPath = '/home/650/resources/Homework1/cranfieldDocs'
		tree = ET.parse(docPath + '/' + docName)
		root = tree.getroot()
		
		docId = root.find('DOCNO').text
		title = root.find('TITLE').text
		author = root.find('AUTHOR').text
		biblio = root.find('BIBLIO').text
		text = root.find('TEXT').text
		# print docId, title
		#create a file 
		files = Document()
		files.add(Field("DOCNO", docId, Field.Store.YES, Field.Index.ANALYZED))
		writer.addDocument(files)
		files.add(Field("TITLE", title, Field.Store.YES, Field.Index.ANALYZED))
		writer.addDocument(files)
		files.add(Field("AUTHOR", author, Field.Store.YES, Field.Index.ANALYZED))
		writer.addDocument(files)
		files.add(Field("BIBLIO", biblio, Field.Store.YES, Field.Index.ANALYZED))
		writer.addDocument(files)
		files.add(Field("TEXT", text, Field.Store.YES, Field.Index.ANALYZED))
		writer.addDocument(files)

	# print "Indexed %d lines from stdin (%d docs in index)" % (n, writer.numDocs())
	# print "Closing index of %d docs..." % writer.numDocs()
	writer.close()

		

	


	# ####get IndexWriterConfig
	

	# # 
	# ####get the writer
	# writer = IndexWriter(indexDir, writerConfig)
	














