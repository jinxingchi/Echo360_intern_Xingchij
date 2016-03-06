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
# import os
import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")
from sklearn.datasets import load_files

##-------------------------------------Take the file name of a test set--------------------------#
argList = sys.argv  #a list of args
# print argList,type(argList)
# data_test = argList[1] #find out the target file
# print doc, 'hahahaha'

##-------------------------------------read in training data ad parse--------------------------#


#work on a partial dataset with only 4 categories
# categories = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']

# twenty_train = load_files("/home/650/resources/Homework2/20ng/20news-bydate-train", categories=categories, shuffle=True, random_state=42)

# print twenty_train.target_names
# print len(twenty_train.data)
# print len(twenty_train.filenames)
# print ("\n".join(twenty_train.data[0].split("\n")[:3]))
# print (twenty_train.target_names[twenty_train.target[0]])

read_data_train = open('/home/650/resources/Homework2/rt-polaritydata/rt-polarity.train', 'rU')
read_data_dev = open('/home/650/resources/Homework2/rt-polaritydata/rt-polarity.dev','rU')
str_train_list = list()
lable_list = list()

for line in read_data_train:
	line = line.split('\n')
	element = line[0].split('\t')
	lable = element[0]
	text = element[1]
	str_train_list.append(text.encode('utf-8'))
	lable_list.append(lable.encode('utf-8'))

lable_numpy = np.array(lable_list)	
# print lable_numpy,'this is lable_numpy'
str_dev_list = list()
lable_list_dev = list()

for line in read_data_dev:
	line = line.split('\n')
	element = line[0].split('\t')
	lable = element[0]
	text = element[1]
	str_dev_list.append(text.encode('utf-8'))
	lable_list_dev.append(lable.encode('utf-8'))

lable_numpy_dev = np.array(lable_list_dev)
# print lable_numpy_dev,'this is lable_numpy_dev'
##---------------------------------------------tokenized with sk-learn----------------------##
# ##Text preprocessing, tokenizing and filtering of stopwords
# count_vect = CountVectorizer()
# X_training_counts = count_vect.fit_transform(str_train_list)
# # print X_training_counts.shape
# # print count_vect.vocabulary_.get(u'algorithm')
# # X_training_counts_dev = count_vect.fit_transform(str_dev_list)

# # ###---------------------------tf idf------------------###
# tf_transformer = TfidfTransformer(use_idf=False).fit(X_training_counts)
# X_train_tf = tf_transformer.transform(X_training_counts)
# print X_train_tf.shape

# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_training_counts)
# # print X_train_tfidf.shape

# # ##-----------------------train naive Bayes classifier-----------##

# NaiveB_clf = MultinomialNB().fit(X_train_tfidf, lable_numpy)

# X_new_counts = count_vect.transform(str_dev_list)
# X_new_tfidf = tfidf_transformer.transform(X_new_counts)
# # print X_new_counts,'this is X_new_counts'
# # print X_new_tfidf,'this is X_new_tfidf',type(X_new_tfidf)
# predicted = NaiveB_clf.predict(X_new_tfidf)
# print np.mean(predicted == lable_numpy_dev),'this is nb mean'

# for doc, category in zip(str_dev_list, predicted):
# 	print('%r => %s' % (doc, lable_numpy[category])),'this is NB hahah'

# ##-----------------------train SVM classifier-----------##

# SVM_clf = SGDClassifier().fit(X_train_tfidf, lable_numpy)

# X_new_counts_svm = count_vect.transform(str_dev_list)
# X_new_tfidf_svm = tfidf_transformer.transform(X_new_counts)
# # print X_new_counts,'this is X_new_counts'
# # print X_new_tfidf_svm,'this is X_new_tfidf_svm',type(X_new_tfidf_svm)
# predicted_svm = SVM_clf.predict(X_new_tfidf_svm)
# # for doc, category in zip(str_dev_list, predicted_svm):
# # 	print('%r => %s' % (doc, lable_numpy[category])),'this SVM hahah'


##--------------building a pipline, pipline class behaves like a compound classifier-------------##
##-----train the model with a single command-----#
#NB model
NaiveB_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])
NaiveB_clf = NaiveB_clf.fit(str_train_list, lable_numpy)
# print NaiveB_clf,'this is NaiveB_clf'
#SVM model
SVM_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier())])
SVM_clf = SVM_clf.fit(str_train_list, lable_numpy)

###------------------------SVM model-------------------------------###

# text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge', penalty='l2'\
# 	,alpha=1e-3, n_iter=5, random_state=42))])
###--------------------using grid search to determine whether unigram, bigram or trigram-----------#
###SVM model parameters 
parameters = {'vect__ngram_range': [(1, 1), (1, 2),(1,3)]\
	,'tfidf__use_idf': (True, False)\
	,'clf__alpha': (1e-2, 1e-3,1e-4,1e-5)\
	,}
gs_clf_svm = GridSearchCV(SVM_clf, parameters, n_jobs=-1)
gs_clf_svm.fit(str_train_list, lable_numpy)
best_parameters, score, _ = max(gs_clf_svm.grid_scores_, key=lambda x: x[1])
for param_name in sorted(parameters.keys()):
    print("%s: %r" % (param_name, best_parameters[param_name]))


print score

#clf__alpha: 0.0001
##tfidf__use_idf: True
#vect__ngram_range: (1, 2)

###NB model parameters

parameters_nb = {'vect__ngram_range': [(1, 1), (1, 2),(1,3)]\
	,'tfidf__use_idf': (True, False)\
	# ,'vect__max_features': (5000, 10000)\
	,'clf__alpha': (0.01, 0.05, 0.1,0.3, 0.5,0.7,0.9, 1),}

gs_clf_nb = GridSearchCV(NaiveB_clf, parameters_nb, n_jobs=-1)
gs_clf_nb.fit(str_train_list, lable_numpy)
best_parameters, score, _ = max(gs_clf_nb.grid_scores_, key=lambda x: x[1])
for param_name in sorted(parameters_nb.keys()):
    print("%s: %r" % (param_name, best_parameters[param_name]))
print score
##clf__alpha: 0.5
##tfidf__use_idf: True
##vect__ngram_range: (1, 2)

##-------------------------------read in test file-------------##
test_file = argList[1]
# print test_file,'this is test_file'
read_data_test = open(test_file,'rU')
str_test_list = list()
lable_list_test = list()

for line in read_data_test:
	# print line,'this is line'
	line = line.split('\n')
	# print line, 'this is split line'
	element = line[0].split('\t')
	lable = element[0]
	text = element[1]
	str_test_list.append(text.encode('utf-8'))
	lable_list_test.append(lable.encode('utf-8'))
# for i in lable_list_test:
# 	print i,'this is i'	
lable_numpy_test = np.array(lable_list_test)		
# print str_test_list,'this is str_test_list'
print lable_numpy_test,'this is lable_list_test'	
# for i in lable_numpy_test:
# 	print i,'this is lable_numpy_test'

NaiveB_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 2),)),\
                     ('tfidf', TfidfTransformer(use_idf=True,)),\
                     ('clf', MultinomialNB()),\
                                           
])

SVM_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 2),)),\
                     ('tfidf', TfidfTransformer(use_idf=True,)),\
                     ('clf', SGDClassifier()),\
                                           
])

NaiveB_clf = NaiveB_clf.fit(str_train_list, lable_numpy)
SVM_clf = SVM_clf.fit(str_train_list, lable_numpy)


predicted_nb = NaiveB_clf.predict(str_test_list)
predicted_svm = SVM_clf.predict(str_test_list)

# print predicted_nb,'this is predicted_nb hahahaha'

print np.mean(predicted_nb == lable_numpy_test),'this is nb mean'
print np.mean(predicted_svm == lable_numpy_test),'this is svm mean'
#0.489589195273 this is nb mean
#0.718626899268 this is svm mean

##---------------------print results---------------------------------###
print '---------- Naive Bayes ----------'

y_true = lable_numpy_test
y_pred = predicted_nb
print y_pred,'this is y_pred'

for i in range(len(y_true)):
	if y_true[i] == '0' and  y_pred[i]=='1':
		print str_test_list[i],'this is false positive'
	if y_true[i] == '1' and  y_pred[i]=='0':
		print str_test_list[i],'this is false negative'	




target_names = ['negative', 'positive']
print(classification_report(y_true, y_pred, target_names=target_names))
print confusion_matrix(y_true,y_pred)
print '\n'
print '---------- SVM ----------'
y_true = lable_numpy_test
y_pred = predicted_svm
target_names = ['negative', 'positive']
print(classification_report(y_true, y_pred, target_names=target_names))
print confusion_matrix(y_true,y_pred)

# for doc in zip(str_test_list, predicted_svm):
	# print('%r => %s' % (doc, lable_numpy_test)),'this SVM hahah'





