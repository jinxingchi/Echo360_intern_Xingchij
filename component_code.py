# -------  This is for seperating component codes into 4 categories ----  #
# ---------  by XJ ------------------#

import csv
import math
import re
import os
import xlrd
import pickle
import pandas as pd

path = os.getcwd()
os.chdir(path)
print 'The current directory is ', path

def find_code(word):
    code = word[word.find('(') + 1:word.find(')')]
    return code



fhand = open('components_by_subsystem.csv', 'rb')
flines = fhand.readlines()
fhand.close()
comp_code = dict()

for line in flines[1:]:
    line = line.strip()
    line = line.split(',')
   
    if len(line[0]) != 0:
        cat = line[0]
        if cat not in comp_code:            
            comp_code[cat] = list()       
        code = find_code(line[1])
        comp_code[cat].append(code)      
    else:        
        code = find_code(line[1])
       
        comp_code[cat].append(code)
        comp_code[cat].sort()


pickle_comp_code = open('comp_code.pickle', 'wb')
pickle.dump(comp_code, pickle_comp_code)
pickle_comp_code.close()
# -- output dataset csv --- #

##output = open('comp_code_output.csv', 'wb')
##writer = csv.writer(output)
##for key, value in comp_code.items():
##    writer.writerow([key, value])
##    
##output.close()


# -------  This is for filtering dataset based on user's selection ----  #
# ------- use pandas ----#
# ---------  by XJ ------------------#




          





            
    
    
