import math
import csv

# resultrows1 = list()
# resultrows2 = list()
countrynames = list()
# key: country name  value: a list of tuples containing 3 numbers
country_dict = dict()

country_name = None
total_population = 0
urban_population = 0
life_exp = 0


fhand1 = open('world_bank_indicators.tsv', 'rU')
file1_line = fhand1.readlines() #read each lines of the indicator file
fhand1.close()
###################################STEP 1####################################
for line in file1_line[1:]:
	line = line.split('\t')
	country_name = line[0].replace('"', '')
	
	if line[9] != '':
		total_population = line[9].replace(',', '').replace('"', '')
		total_population = float(total_population)
	else:
		total_population = ''
	if line[10] != '':
		urban_population = line[10].replace(',', '').replace('"', '')
		urban_population = float(urban_population)
	else:
		urban_population = ''
	if line[14] != '':
		life_exp = line[14].replace(',', '').replace('"', '')
		life_exp = int(line[14])
	else:
		life_exp = ''
	if country_name not in country_dict:
		country_dict[country_name] = [(total_population, urban_population, life_exp)]
	else:
		country_dict[country_name].append((total_population, urban_population, life_exp))

# print sorted(country_dict.keys())
############calculate the average urban population ratio.

tot_urbanpop_dict = dict() #for step 2
ave_urbanpop_dict = dict()

# loop over every items key:country names value: selected columns
for k in country_dict:
	tot_totalpop = 0
	tot_urbanpop = 0
	tot_lifeexp = 0
	urbanpop_rate = 0
	ave_lifeexp = 0
	tot_count = 0
	# urbanpop_rate = []
	# loop over each country to get the totpop and urbanpop
	for i in country_dict[k]:
		if i[0] != '':
			tot_totalpop += i[0]
		if i[1] != '':
			tot_urbanpop += i[1]	
		if i[2] != '':		
			tot_lifeexp += i[2]
			tot_count += 1

	urbanpop_rate = float(tot_urbanpop/tot_totalpop)
	if tot_count != 0:
		ave_lifeexp = float(tot_lifeexp)/float(tot_count)
	else:
		ave_lifeexp = 0
	tot_urbanpop_dict[k] = (urbanpop_rate, ave_lifeexp, tot_totalpop, tot_urbanpop)
	ave_urbanpop_dict = tot_urbanpop_dict # for step 2
	# drop missing values
	if tot_totalpop == 0 or tot_urbanpop == 0 or tot_lifeexp == 0:
		del ave_urbanpop_dict[k]
	# elif tot_lifeexp == 0:
			


			# print len(country_dict[k]), i[2], tot_lifeexp,len(country_dict[k])
	# elif k in ave_urbanpop_dict.keys():
	# 	del ave_urbanpop_dict[k]
	#else:
		# ave_urbanpop_dict[country_name].append(float(urbanpop_rate)
# print sorted(ave_urbanpop_dict.keys())
output = open('si601_w16_hw1_step1_xingchij.csv', 'w')
csv_output = csv.writer(output)
# header
csv_output.writerow(['country name', 'average urban population ratio', 'average life expectancy', 'sum of total population in all years', 'sum of urban population in all years'])

for c in sorted(ave_urbanpop_dict.keys()):
	csv_output.writerow([c,ave_urbanpop_dict[c][0], ave_urbanpop_dict[c][1], ave_urbanpop_dict[c][2], ave_urbanpop_dict[c][3]])
output.close()

###################################STEP 2####################################
fhand2 = open('world_bank_regions.tsv', 'rU')
file2_line = fhand2.readlines()
fhand2.close()
region_dict = dict()
region_name = None

for line in file2_line:
	line = line.strip()
	line = line.replace('"', '').replace('\n', '').replace(',', '').split('\t')
	region_name = line[0]
	# print region_name
	if region_name not in region_dict:
		region_dict[region_name] = line[2:]
	else:
		region_dict[region_name] += line[2:]
# print region_dict.items()
for region in region_dict.keys():
	tot_regionpop = 0
	tot_reg_ubpop = 0
	region_ubpop_rate = 0
	tot_reg_country = 0
	tot_reg_lifexp = 0
	for country_key in region_dict[region]:
		if country_key in tot_urbanpop_dict.keys():
			tot_regionpop += tot_urbanpop_dict[country_key][2]
			tot_reg_ubpop += tot_urbanpop_dict[country_key][3]
			# tot_reg_country += 1
			tot_reg_lifexp += tot_urbanpop_dict[country_key][1]

# calculate the number of countries with non-missing total population number
			if tot_reg_lifexp != 0:
				tot_reg_country += 1
			else:
				tot_reg_country = tot_reg_country	

	if tot_regionpop != 0:
		region_ubpop_rate = float(tot_reg_ubpop)/float(tot_regionpop)
	else:
		region_ubpop_rate = 0
	if tot_reg_country != 0:
		ave_reg_lifexp = float(tot_reg_lifexp)/float(tot_reg_country)
	else:
		ave_reg_lifexp = 0
	region_dict[region] = [region_ubpop_rate, ave_reg_lifexp]
	# print ave_reg_lifexp

###############################write the csv##################
output2 = open('si601_w16_hw1_step2_xingchij.csv', 'w')
csv_output2 = csv.writer(output2)
# header of the csv
csv_output2.writerow(['region', 'average urban population ratio', 'average life expectancy'])

# output the csv
# for c in sorted(region_dict.keys(), key = lambda x: x[2], reverse = True):
# 	csv_output2.writerow([c,region_dict[c][0], region_dict[c][1]])
# output2.close()

for c, v in sorted(region_dict.items(), key = lambda (x, y): y[1], reverse = True):
	csv_output2.writerow([c,region_dict[c][0], region_dict[c][1]])
output2.close()



	



