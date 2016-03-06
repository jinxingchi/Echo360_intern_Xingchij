import re
import json
import simplejson as json
from pyspark import SparkContext
import sys

#path : /user/yuhangw/yelp_academic_dataset.json
#neighborhood,city, 273 businesses,total review count,average star rating.
sc = SparkContext(appName = "HW5")
# input_file = sc.textFile("hdfs:///user/yuhangw/yelp_academic_dataset_business.json")
input_file = sc.textFile("hdfs:///user/yuhangw/yelp_academic_dataset.json")

def nbh_map(data):
  stars = data.get('stars', None)
  reviews = data.get('review_count', None)
  city = data.get('city', None)
  nbhs = data.get('neighborhoods', None)
  nbh_list = list()
  if nbhs:
    for n in nbhs:
      nbh = tuple()
      nbhVal = list()
      nbhID = (city, n)
      # if reviews != None:
      nbhVal.append(reviews)
      # else:
      #   nbhVal.append(0)
      # if stars != None:
      nbhVal.append(stars)
      # else:
      #   nbhVal.append(0)
      nbhVal.append(1)
      nbh = (nbhID, nbhVal) 
      nbh_list.append(nbh)
      # nbh + (nbhID,)
      # nbh + (nbhVal,)
  else:
    nbh = tuple()
    nbhVal = list()
    nbhID = (city,'Unknown')
    # if reviews != None:
    nbhVal.append(reviews)
    # else:
    #   nbhVal.append(0)
    # if stars != None:
    nbhVal.append(stars)
    # else:
    #   nbhVal.append(0)
    nbhVal.append(1)
    nbh = (nbhID, nbhVal)  
    # nbh + (nbhID,)
    # nbh + (nbhVal,)
    nbh_list.append(nbh)

  return nbh_list


nbh_list = input_file.map(lambda line: json.loads(line))\
          .filter(lambda x : x.get('type','') == 'business')\
          .flatMap(nbh_map)\
          .reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]))\
          .map(lambda x: (x[0][0], x[0][1], x[1][2], x[1][0], x[1][1]/x[1][2]))\

nbh_list_sorted = nbh_list.sortBy(lambda x: (x[0], -x[2], -x[3]))
nbh_list_sorted.map(lambda t : t[0] +'\t'+ t[1] +'\t'+str(t[2]) + '\t'+str(t[3]) +'\t'+ str(t[4]))\
          .saveAsTextFile('spark_neighbourhood_output')
# nbh_list.map(lambda t : t[0] +'\t'+ t[1] + '\t'+str(t[2]) + '\t'+str(t[3]) +'\t'+ str(t[4])).saveAsTextFile('spark_neighbourhood_output')
# x[0][0] + y[0][0], x[0][1] + y[0][1]
          # .mapValues(lambda x: x.append(1))\
nbh_list_sorted.collect()

