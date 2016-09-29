# **************************************************************************** #
# ----------------------------  Data Analysis   -------------------------------#
# **************************************************************************** #
import sys, getopt
import xlrd
import pickle
import pandas as pd
import numpy as np
import os

path = os.getcwd()
os.chdir(path)

# **************************************************************************** #
# --------  read in and filter packed claim data based on user input ----------#
# **************************************************************************** #

## read in claim data ##

def read_org_claim():
    
    pickle_claim_data = open('claim_data.pickle', 'rb')
    df_claim = pickle.load(pickle_claim_data) ## claim data is in DataFrame type and ungrouped. ##
    df_claim.production_month = pd.to_datetime(df_claim.production_month, \
                                                format = '%Y/%m')
    return df_claim
#print 'claim data unpacked. '

## read in production volume data ##
pickle_vol_data = open('vol_data.pickle', 'rb')
df_volGrp = pickle.load(pickle_vol_data) ## vol data is in DataFrame type and grouped. ##
#print df_volGrp
df_volGrp.ProdMth = pd.to_datetime(df_volGrp.ProdMth, \
                                            format = '%Y/%m')


#print 'Production volume data unpacked. '


# **************************************************************************** #
# -------- get baseline dataset (2015/01- 2015/05) = mu +- sigma --------------#
# **************************************************************************** #
def set_baseline():
    df_claim = read_org_claim()
    ## global values (will from user's settings) ##
    DATA_PERIOD = 6

    ## find the most recent month in claim dataset ##
    currentMon = df_claim['production_month'].max()
    ## set the first baseline months to be 16 months prior to prod_month ##
    BSL_SET = 12
    PERIOD_MTH = 1    
    ## find the baseline months ##
    m = BSL_SET
    BSL_MTH = list()
    ## I change m>= 7 from m >= 8 to make the baseline months to be 6 months ##
    while m >= 7:
        baseline_month = pd.to_datetime(currentMon, format = '%Y/%m')\
                         - pd.DateOffset(months = m)
        
        BSL_MTH.append(baseline_month)
        m = m - 1
        
    print BSL_MTH, 'this is inside baseline month'
    return BSL_MTH


def claimRateCal(monthUsr,cateUsr):
    ## filter month = user define production month + baseline month
   # monthUsr = pd.to_datetime(monthUsr)
    #print monthUsr, 'this is monthUsr'
    df_claim = read_org_claim()
    monthUsr = pd.to_datetime(monthUsr, format = '%Y/%m')
    monthBsl = set_baseline()

  
    #monthFil = monthUsr + monthBsl
    monthFil = monthBsl + [monthUsr]
    ##print monthFil, 'this is monthFil'
    month_ts = pd.Series(monthFil)
    
    ## filter the claim data based on factors: production month & category
    df_claim.loc[:,'count'] = [1 for i in range(len(df_claim['brand_code']))]
    
    claimFil = df_claim[(df_claim['production_month'].isin(month_ts)) &\
                                          (df_claim['category'] == cateUsr)]

    ## group the claim data. each unit is like: prod mth--brandcode--component--claim mth--claim count
    claimFil.claim_month = pd.to_datetime(claimFil.claim_month, format='%Y/%m')

    claimGrp = claimFil[['production_month','brand_code','service_component_code','claim_month','count']].\
            groupby(['production_month','brand_code','service_component_code','claim_month',\
                     pd.Grouper(key='claim_month',freq='MS')], as_index=False)['count'].count()

    ## filter the production volume data based on factor: production month
    volFil = df_volGrp[df_volGrp['ProdMth'].isin(month_ts)]

    claimRate = volFil

    ## map the filtered production data to filtered claim data
    dic_volGrp = dict(zip(zip(volFil.ProdMth,volFil.brand_code),volFil.Volume))

    claimGrp['mapKey'] = zip(claimGrp['production_month'],claimGrp['brand_code'])
    claimGrp['volume'] = claimGrp['mapKey'].map(dic_volGrp)

    col = claimGrp.columns.tolist()
    claimRate = claimGrp[[col[0],col[1],col[2],col[3],col[4],col[6]]]
    claimRate.loc[:,'SIR_comp'] = claimRate['count']/claimRate['volume']
  
    return claimRate




def cumulRateCal(mthlyRate):
    cumulRate = mthlyRate
    cumulTemp = cumulRate.groupby(['production_month','brand_code','service_component_code'], \
                      as_index=False)['SIR_comp'].cumsum(axis = 0)
    cumulRate['SIR_comp'] = cumulTemp
    ##print 'thhis is insiede cumulrate'
    
    return cumulRate

def claimAnalyze(monthUsr, cateUsr):
    claimRate = claimRateCal(monthUsr, cateUsr)
    claimRate = cumulRateCal(claimRate)
  #  print 'this is inside c_a claimrate'
   ## --------------------------------------------  THis is right -------------------------##
##    print ' ------ START cumulRateCal -----'
##    print claimRate[(claimRate['brand_code'] == 'KAD582') \
##                    & (claimRate['service_component_code'] == '331')]
##    print '------- END OF claimRate -------'
    pickle_claimRate = open('claimRate.pickle','wb')
    pickle.dump(claimRate, pickle_claimRate)
    pickle_claimRate.close()







