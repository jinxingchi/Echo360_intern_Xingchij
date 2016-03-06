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
import csv
import re
import nltk
from nltk.stem import *
from nltk.stem.porter import *
# from nltk import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

# from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
#module load python
#source activate ir

#python b.py train.csv unlabeled_test.csv a.csv
reload(sys)
sys.setdefaultencoding("ISO-8859-1")

argList = sys.argv  #a list of args
stemmer = SnowballStemmer("english")
atSign = re.compile(r'@[a-zA-Z0-9]+')
isURL = re.compile(r'http:[a-zA-Z0-9\/\.]+')
# isP = re.compile(r':P')

##-------------------- read in training data----------------##
train_data = argList[1]

# path = '/home/xingchij/hidden/1740225059/Homework2'
# read_train = open(path + '/'+train_data, 'rU')
read_train = open(train_data, 'rU')
str_train_list = list()
lable_list = list()
stemWordList = list()


for line in read_train:
	line = line.strip()
	# print line
	element = line.split(',')
	lable = element[0]
	user_id = element[1].replace('"','')
	text = element[5]
	if atSign.search(text) != None:
		text = re.sub(r'(@[a-zA-Z0-9]+)', '',text.lower())
	if isURL.search(text) != None:
		text = re.sub(r'(http:[a-zA-Z0-9\/\.]+)', 'url',text.lower())	
	# # print text,'thsi is text'		
	# token_list = nltk.word_tokenize(text) #tokenizing
	# # print token_list,'this is token_list,jinjinijnxingxing'
	# # print type(token_list)
	# # stemText = list()
	# stemText = ''
	# for token in token_list:
	# 	# print token,'this is token'	
	# 	tokenStem = stemmer.stem(token)  #stemming
	# 	# print tokenStem,'this is tokenStem, hahahahhhhhhh'
	# 	stemText= stemText + ' ' + tokenStem
	# 	# stemWordList.append(tokenStem)
	# 	# print stemText,'this is stemText,hahahhahaahha',len(stemText)
	# 	# str_train = ' '.join(stemText)
	# # print stemText, 'this is stemText,yiyayiyahouyiyayiyahou'
	# # print str_train, 'this is str_train',type(str_train)
	str_train_list.append(text.encode('utf-8'))
	# str_train_list.append(text.encode('utf-8'))
	# print lable,user_id,text
	# str_train_list.append(text.encode('utf-8'))
	lable_list.append(lable.encode('utf-8'))

lable_numpy = np.array(lable_list)
# print lable_numpy

#------------------------------------use NB model ----------------------##
#NB model
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(str_train_list)
select = SelectKBest(chi2, k=1000)
X_new = select.fit_transform(X_train_counts, lable_numpy)
print X_new.shape, lable_numpy.shape
# NaiveB_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])
# NaiveB_clf = NaiveB_clf.fit(str_train_list, lable_numpy)
NaiveB_clf = MultinomialNB().fit(X_new, lable_numpy)
# SVM_clf = SGDClassifier().fit(X_new, lable_numpy)


# # SVM_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier())])
# # SVM_clf = SVM_clf.fit(str_train_list, lable_numpy)

# ##NB model parameters selection

# parameters_nb = {'vect__ngram_range': [(1, 1), (1, 2),(1,3)]\
# 	,'tfidf__use_idf': (True, False)\
# 	# ,'vect__max_features': (5000, 10000)\
# 	,'clf__alpha': (0.01, 0.05, 0.1,0.3, 0.5,0.7,0.9, 1),}

# gs_clf_nb = GridSearchCV(NaiveB_clf, parameters_nb, n_jobs=-1)
# gs_clf_nb.fit(str_train_list, lable_numpy)
# best_parameters, score, _ = max(gs_clf_nb.grid_scores_, key=lambda x: x[1])
# for param_name in sorted(parameters_nb.keys()):
#     print("%s: %r" % (param_name, best_parameters[param_name]))
# print score


# parameters = {'vect__ngram_range': [(1, 1), (1, 2),(1,3)]\
# 	,'tfidf__use_idf': (True, False)\
# 	,'clf__alpha': (1e-2, 1e-3,1e-4,1e-5)\
# 	,}
# gs_clf_svm = GridSearchCV(SVM_clf, parameters, n_jobs=-1)
# gs_clf_svm.fit(str_train_list, lable_numpy)
# best_parameters, score, _ = max(gs_clf_svm.grid_scores_, key=lambda x: x[1])
# for param_name in sorted(parameters.keys()):
#     print("%s: %r" % (param_name, best_parameters[param_name]))


# print score

##-------------------------------read in test file-------------##
test_file = argList[2]
# print test_file,'this is test_file'
read_data_test = open(test_file,'rU')
str_test_list = list()
lable_list_test = list()
user_idList = list()

for line in read_data_test:
	# print line,'this is line'
	line = line.strip()
	# line = line.split(',')
	# print line, 'this is split line'
	element = line.split(',')
	# print element
	# lable = element[0]
	user_id = element[0].replace('"','')
	text = element[4]
	# if atSign.search(text) != None:
	# 	text = re.sub(r'^(@[a-zA-Z0-9]+)', '',text.lower())
	# if isURL.search(text) != None:
	# 	text = re.sub(r'(http:[a@-zA-Z0-9\/\.]+)', 'url',text.lower())	
	# # print text,'thsi is text'		
	# token_list = nltk.word_tokenize(text) #tokenizing
	# # print token_list,'this is token_list,jinjinijnxingxing'
	# # print type(token_list)
	# # stemText = list()
	# # for token in token_list:
	# # 	# print token,'this is token'	
	# # 	tokenStem = stemmer.stem(token)  #stemming
	# # 	# print tokenStem,'this is tokenStem, hahahahhhhhhh'
	# # 	stemText.append(tokenStem)
	# # 	# stemWordList.append(tokenStem)
	# # 	# print stemText,'this is stemText,hahahhahaahha',len(stemText)
	# # 	str_test = ' '.join(stemText)
	# stemText = ''
	# for token in token_list:
	# 	# print token,'this is token'	
	# 	tokenStem = stemmer.stem(token)  #stemming
	# 	# print tokenStem,'this is tokenStem, hahahahhhhhhh'
	# 	stemText= stemText + ' ' + tokenStem	


	user_idList.append(user_id)
	str_test_list.append(text.encode('utf-8'))
	lable_list_test.append(lable.encode('utf-8'))

X_test_counts = count_vect.transform(str_test_list)
X_new_test = select.transform(X_test_counts)



# NaiveB_clf = NaiveB_clf.fit(str_train_list, lable_numpy)
# SVM_clf = SVM_clf.fit(str_train_list, lable_numpy)


predicted_nb = NaiveB_clf.predict(X_new_test)
# predicted_svm = SVM_clf.predict(str_test_list)
# print predicted_nb,'this is predicted_nb'
# print predicted_nb,'this is predicted_nb hahahaha'
# print 'I am gone through the read test data'
output_file = argList[3]
output = open(output_file, 'w')
csv_output = csv.writer(output)
# header of the csv
# print 'I am writerow'
csv_output.writerow(['ID', 'Predicted_label'])
for i in range(len(predicted_nb)):
	# print 'this is i'
	csv_output.writerow([user_idList[i],predicted_nb[i].replace('"','')])
output.close()










