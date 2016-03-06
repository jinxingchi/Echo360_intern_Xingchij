import re
import urlparse
import csv

################################STEP 1###########################
validLines = list()
invalidLines = list()
invalidIpDict = dict()
# 2 types of valid url
def is_valid(line):
	isValid1 = False
	isValid2 = False
	valid = False
	line = line.strip()
	type1 = re.compile(r'^[\d\.]+[\s-]+.*"(GET|POST|HEAD)\s*([Hh][Tt][Tt][Pp][Ss]?://.*)"\s*[235]\d*.*')
	type2 = re.compile(r'^[\d\.]+[\s-]+.*"CONNECT.*"\s*[235]\d.*')

	if type1.search(line):
		url = type1.search(line).group(2)
		parseResult = urlparse.urlparse(url)  #this would return a 6 tuple
		queryString = parseResult[4]          #find query string
		qsResult = urlparse.parse_qs(queryString)   #get key value pair
		# print len(qsResult.values())
		if len(qsResult) == 0:
			isValid1 = True
		else:	
			for i in qsResult.values():
				# print i
				if len(i[0]) <= 80:
					# print i
					isValid1 = True
				if len(i[0]) > 80:
					# print i, 'hahahaha'
					isValid1 = False
					break	
		
	elif type2.search(line):
		isValid2 = True
	if isValid1 == True or isValid2 == True:
		valid = True
	else: 
		valid = False	
	return valid
#####################return the client IP address###########
def extract_ip(line):
	line = line.strip()
	ip_compile = re.compile(r'^([\d\.]+).*')
	ip = ip_compile.search(line).group(1)
	return ip

##########read file########################
fhand = open('access_log.txt','rU')
sourceLine = fhand.readlines()
fhand.close()	

for l in sourceLine:
	result = is_valid(l)
	if result == True:
		validLines.append(l)
	if result == False:
		invalidLines.append(l)
#write files
output1 = open('valid_access_log_xingchij.txt', 'w')
for i in validLines:
	output1.writelines(i)
output1.close()

output2 = open('invalid_access_log_xingchij.txt', 'w')
for j in invalidLines:
	output2.writelines(j)
output2.close()	
# print (len(validLines) + len(invalidLines))
# print validLines[48]
for i in invalidLines:
	suspectIp = extract_ip(i)
	# print suspectIp
	if suspectIp in invalidIpDict.keys():
		invalidIpDict[suspectIp] += 1
	if suspectIp not in invalidIpDict.keys():
		invalidIpDict[suspectIp] = 1	
output3 = open('suspicious_ip_summary_xingchij.csv', 'w')
csv_output3 = csv.writer(output3)
csv_output3.writerow(['IP Address','Attempts'])
for k,v in sorted(invalidIpDict.items(),key = lambda x: x[1], reverse = True):
	csv_output3.writerow([k,v])
output3.close()	