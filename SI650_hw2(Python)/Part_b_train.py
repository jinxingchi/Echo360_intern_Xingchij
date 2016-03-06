import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

#python b.py training_set.csv test_set.csv prediction_file
import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")

argList = sys.argv  #a list of args

##-------------------- read in training data----------------##
train_data = argList[1]
path = '/home/xingchij/hidden/1740225059/Homework2'
read_train = open(path + '/'+train_data, 'rU')

for line in read_train:
	line = line.split('\n')
	print line
	element = line[0].split('\t')
	lable = element[0]
	text = element[1]
	str_train_list.append(text.encode('utf-8'))
	lable_list.append(lable.encode('utf-8'))