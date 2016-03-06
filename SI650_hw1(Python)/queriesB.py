import sys
import lucene
import utils
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
 
if __name__ == "__main__":
    lucene.initVM()
    analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
    reader = IndexReader.open(SimpleFSDirectory(File("Index")))
    searcher = IndexSearcher(reader)
    argList = sys.argv  #a list of args
    # print argList,type(argList)
    document = argList[1] #find out the target file
    # print doc, 'hahahaha'
    # dirs = os.listdir(doc) #get al
    docPath = '/home/650/resources/Homework1/'
    readFile = open(document, 'rU')
    for line in readFile:
        # print line
        query = QueryParser(Version.LUCENE_4_10_1, "TEXT", analyzer).parse(line)
        MAX = 1000
        hits = searcher.search(query, MAX)
        docIdList = list()

        # print 'end of line'
    # print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
        for hit in hits.scoreDocs:


            # print 'hahahahaha'
            # print hit.score, hit.doc, hit.toString()
            doc = searcher.doc(hit.doc)
            docId = doc.get("DOCNO").encode("utf-8").strip()
            docTitle = doc.get("TITLE").encode("utf-8").strip()
            if docId not in docIdList:
                docIdList.append(docId)        
        # for i in docIdTitleList:
                utils.print_lucene_hit(docId, docTitle, hit.score)            
