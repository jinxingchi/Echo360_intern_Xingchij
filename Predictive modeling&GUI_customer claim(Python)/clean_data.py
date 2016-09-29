import sys, getopt
import xlrd
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import os
import data_plot as d_p

path = os.getcwd()
os.chdir(path)
print 'The current directory is ', path

## --------------       open component code dictionary pickle      -----------#
pickle_comp_code = open('comp_code.pickle', 'rb')
comp_code = pickle.load(pickle_comp_code)

## declare global variables of brand_code ##
TG_BRAND_CODE = ['AMA583', 'AMA584', 'AMA773', 'JEN582'\
                 , 'JEN586', 'IKE582', 'IKE583', 'IKE773'\
                 , 'KAD582', 'KAD596', 'KAD773', 'MAY714'\
                 , 'MAY814', 'WHR582', 'WHR583', 'WHR584'\
                 , 'WHR772', 'WHR773']


## The map_category function is for creating a new column in the dataset
## with category from the dictionary

def map_category(data):
    cat = ''
    data = str(data)
  
    if data in comp_code['Wash']:
        cat = 'Wash'

    elif data in comp_code['Documentation']:
        cat = 'Documentation'
    elif data in comp_code['Structures']:
        cat = 'Structures'
    elif data in comp_code['Controls']:
        cat = 'Controls'
    else:
        cat = 'NA'
    return cat

# **************************************************************************** #
# -----------  read in excel file and create new columns   --------------------#
# **************************************************************************** #

def set_period(dataframe):
    ## global values (will from user's settings)
    DATA_PERIOD = 6

    ## find the most recent month in claim dataset ##
    currentMon = dataframe['production_month'].max()
    ## set the first baseline months to be 12 months prior to prod_month
    PERIOD_SET = 12
    PERIOD_MTH = 1    
    ## find the baseline months
    m = PERIOD_SET
    PERIOD_MTH = list()
    while m >= 0:
        valid_month = pd.to_datetime(currentMon, format = '%Y/%m')\
                         - pd.DateOffset(months = m)
        
        PERIOD_MTH.append(valid_month)
        m = m - 1
##    print '--------- THIS IS VALID PERIOD ----------'
##    print PERIOD_MTH
##    print '-------- END OF VALID PERIOD -------------'
    return PERIOD_MTH    



def parse_dataset(dataset):
    
    df_claim = pd.read_excel(dataset)

    ## leave only the latest one year 
    df_claim.production_month = pd.to_datetime(df_claim.production_month, \
                                                format = '%Y/%m')

    
    ##create a new column using brand + code
    period_month = set_period(df_claim)
    df_claim['brand_code'] = df_claim['brand'] + df_claim['product_code'].map(str)
    df_claim['service_component_code'] =  df_claim['service_component_code'].astype(str)

    ## filter dataset based on brand_code and part_sequence
 
    df_claim = df_claim.loc[(df_claim['brand_code'].isin(TG_BRAND_CODE)) \
                            & (df_claim['part_sequence'] == 1)\
                            & (df_claim['production_month'].isin(period_month))]
    
##    print ' ********* THIS IS original DF_CLAIM ***********'
##    print df_claim
##    print ' ********* END OF original DF_CLAIM ************'    
    
    ## create a new column 'category'
    df_claim['category'] = map(map_category, df_claim['service_component_code'])
    pickle_claim_data = open('claim_data.pickle', 'wb')
    pickle.dump(df_claim, pickle_claim_data)
    pickle_claim_data.close()

    return df_claim


# **************************************************************************** #
# -----------  read in volume file and create new columns   --------------------#
# **************************************************************************** #

def getTotalVolume(volumeData):
    
    df_vol = pd.read_excel(volumeData)
    df_vol['brand_code'] = df_vol['Brand'] + df_vol['Product Code'].map(str)

    ## filter dataset based on brand_code

    df_vol = df_vol.loc[df_vol['brand_code'].isin(TG_BRAND_CODE)]

    #print df_vol.dtypes
 
    vol_grp = df_vol.groupby(['ProdMth','brand_code'], as_index=False)['Volume'].sum()
    pickle_vol_data = open('vol_data.pickle', 'wb')
    pickle.dump(vol_grp, pickle_vol_data)
    pickle_vol_data.close()
    #print 'Production volume data packed as: vol_data.pickle.'
    return vol_grp
    
#print type(vol_grp.get_group(('2014/01','AMA583')))
#print vol_grp.get_group(('2014/01','AMA583')).sum()
## use 'total_vol.xlsx' for testing


def loadData():
    
    getTotalVolume('total_vol.xlsx')
    parse_dataset('claimset.xlsx')
    TIMELIST = d_p.set_prodList()
    print "data loaded"
    return TIMELIST
    
'''
print '-------- GET TOTAL DATA ---------------'    
print getTotalVolume('total_vol.xlsx')
print '-------------- END ---------------------'
'''

'''
print '-------- GET CLAIM DATA ---------------' 
print parse_dataset('claimset.xlsx')
print '-------- END CLAIM DATA ---------------' 

'''

