import sys
import numpy as np
import csv

reload(sys)
sys.setdefaultencoding("ISO-8859-1")

argList = sys.argv
train_data = argList[1]   #read train.csv
# print train_data

def findPolar(string):
	path = '/home/xingchij/hidden/1740225059/Homework2'
	read_train = open(path + '/'+train_data, 'rU')

	str_train_list = list()
	lable_list = list()

	for line in read_train:
		line = line.strip()
		element = line.split(',')
		lable = element[0]
		user_id = element[1]
		text = element[5]
		str_train_list.append(text.encode('utf-8'))
		lable_list.append(lable.encode('utf-8'))
	# print str_train_list
	n_0 = 0
	n_4 = 0
	for i in lable_list:
		# print type(i),'this is i'
		if i == '0':
			n_0 += 1
		elif i == '4':
			n_4 += 1
	if n_0 > n_4:
		return	'0'
	elif n_0 <= n_4:
		return '4'			


test_file = argList[2]
path = '/home/xingchij/hidden/1740225059/Homework2'
read_data_test = open(path + '/'+test_file,'rU')
outputList = list()
print 'I am ready to read test data'
for line in read_data_test:
	# print line,'this is line'
	line = line.strip()
	# print line, 'this is split line'
	element = line.split(',')
	user_id = element[0].replace('"','')
	print user_id,'this is user_id'
	text = element[4]
	predicted_lable = findPolar(text)
	print predicted_lable,'this is predicted_lable'
	# predicted_lableList.append(predicted_lable)
	outputList.append([user_id,predicted_lable])
# 	user_idList.append(user_id)
# 	str_test_list.append(text.encode('utf-8'))
# 	lable_test_list.append(lable.encode('utf-8'))
# # lable_numpy_test = np.array(lable_list_test)	
# predicted_lableList = list()	

	# predicted_lable = findPolar(i)
	# predicted_lableList.append(predicted_lable)
print 'I am gone through the read test data'
output_file = argList[3]
output = open(output_file, 'w')
csv_output = csv.writer(output)
# header of the csv
print 'I am writerow'
csv_output.writerow(['ID', 'Predicted_label'])
for i in outputList:
	print 'this is i'
	csv_output.writerow(i)
output.close()





