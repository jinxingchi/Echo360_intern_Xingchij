## ------------- MODIFIED ------------------------------------------##
# This script has modified baseline months to 12 months ahead of  --##
## month -----------------------------------------------------------##

import sys, getopt
import xlrd
import pickle
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
#style.use('fivethirtyeight')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import Tkinter as Tk
import os
import claim_analysis as c_a

path = os.getcwd()
os.chdir(path)

## -------------- global values (will from user's settings) ------  ##
DATA_PERIOD = 6

## set the first baseline months to be 12 months ahead of prod_month
BSL_SET = 12
#PERIOD_MTH = 1
BSL_MTH = c_a.set_baseline()

TG_BRAND_CODE = ['AMA583', 'AMA584', 'AMA773', 'JEN582'\
                 , 'JEN586', 'IKE582', 'IKE583', 'IKE773'\
                 , 'KAD582', 'KAD596', 'KAD773', 'MAY714'\
                 , 'MAY814', 'WHR582', 'WHR583', 'WHR584'\
                 , 'WHR772', 'WHR773']

##pickle_comp_code = open('comp_code.pickle', 'rb')
##comp_code = pickle.load(pickle_comp_code)
## read in claim data ##
def read_in():
    pickle_claim_rate = open('claimRate.pickle', 'rb')
    claimRate = pickle.load(pickle_claim_rate)
    claimRate.production_month = pd.to_datetime(claimRate.production_month, \
                                                format = '%Y/%m')
    claimRate.claim_month = pd.to_datetime(claimRate.claim_month, \
                                                format = '%Y/%m')
    claimRate['claim_month'] = claimRate['claim_month'].apply(lambda x: x.replace(day = 1))
   
    return claimRate

def baseLineCal(claimRate, prodUsr, compntUsr):
    ## find the baseline months
    ##BSL_MTH = c_a.set_baseline()

    ## filter claim rate data
    claimBsl = claimRate[(claimRate['production_month'].isin(BSL_MTH)) & \
                         (claimRate['brand_code'] == prodUsr) & \
                         (claimRate['service_component_code'] == compntUsr)]

    compntBsl = pd.DataFrame(columns=['prodID','compntID','period'\
                                      ,'avg_SIR','std_SIR+','std_SIR-'])
    
    period = 1
    while period <= DATA_PERIOD:
        bslTemp = pd.DataFrame(columns=['prodMth','period','SIR'])
        for month in BSL_MTH:
            nextMth = pd.to_datetime(month) + pd.DateOffset(months = period)
            #print nextMth, 'next' 
            tgData = claimBsl[(claimBsl['production_month'] == month) & \
                                (claimBsl['claim_month'] == nextMth)]
            
            while (nextMth > month) & tgData.empty:
                nextMth = nextMth - pd.DateOffset(months = 1)
                tgData = claimBsl[(claimBsl['production_month'] == month) & \
                                (claimBsl['claim_month'] == nextMth)]

            if tgData.empty:
                newLine = pd.DataFrame([[month,period,0]],columns=['prodMth','period','SIR'])
                bslTemp = bslTemp.append(newLine)

            else:
                value = tgData['SIR_comp'].values[0]
                newLine = pd.DataFrame([[month,period,value]],columns=['prodMth','period','SIR'])
                bslTemp = bslTemp.append(newLine)

        meanVal = bslTemp['SIR'].mean()
        ## calculate baseline and upper, lower boundaries
        stdValPos = bslTemp['SIR'].mean() + bslTemp['SIR'].std()
        stdValNeg = bslTemp['SIR'].mean() - bslTemp['SIR'].std()

        ##set lower level to zero if it is negative
        if stdValNeg < 0:
            stdValNeg = 0
        ## add them to dataframe
        newLine = pd.DataFrame([[prodUsr,compntUsr,period,meanVal*1000000,stdValPos*1000000,stdValNeg*1000000]],\
                            columns=['prodID','compntID','period','avg_SIR','std_SIR+','std_SIR-'])
        compntBsl = compntBsl.append(newLine)   
        period = period + 1
            
    #print compntBsl, 'this is compnBSL'
    return compntBsl


## This function is for calculating the SIR line of target component ##
def compntLineCal(claimRate, compntMth, prodUsr, compntUsr):
    compntLine = pd.DataFrame(columns=['prodMth','period','SIR'])
    
    compntMth = pd.to_datetime(compntMth)
    claimCpt = claimRate[(claimRate['production_month'] == compntMth) & \
                         (claimRate['brand_code'] == prodUsr) & \
                         (claimRate['service_component_code'] == compntUsr)]
##    print '------------ This is for debugging compntLineCal--------------'
##    print claimCpt
##    print '---------------- end of compntLineCal --------------'

    period = 1
    
    while period <= DATA_PERIOD:
        nextMth = compntMth + pd.DateOffset(months = period)
        tgData = claimCpt[(claimCpt['claim_month'] == nextMth)]
##        print '----- tgData -----'
##        print tgData
##        print '-------- end of tg Data -----'
       
        ## The while loop is for finding the cumul SIR when there is a missing month ##
        while (nextMth > compntMth) & tgData.empty:
            nextMth = nextMth - pd.DateOffset(months = 1)
            tgData = claimCpt[(claimCpt['claim_month'] == nextMth)]

        ## If all months until the present month are missing ##
        if tgData.empty:
            newLine = pd.DataFrame([[compntMth,period,0]],columns=['prodMth','period','SIR'])
            compntLine = compntLine.append(newLine)
            
        else:
            value = tgData['SIR_comp'].iloc[-1]
##            print '--------- this is tgData values[0]----- '
##            print tgData['SIR_comp'].values
##            print '----------- end of this is tgData values ---'
            newLine = pd.DataFrame([[compntMth,period,value*1000000]],columns=['prodMth','period','SIR'])
            compntLine = compntLine.append(newLine)
        period = period + 1   
    
    return compntLine


def set_compntList(cateUsr):
    compntList = comp_code[cateUsr]
    return compntList

## set color of the button on UI ##
def set_color(monthUsr, cateUsr):

    ## read from pickle file or from scratch ##
    if ('color_'+monthUsr+'_'+cateUsr+'.pickle') in (os.listdir(path)):
        pickle_color = open(('color_'+monthUsr+'_'+cateUsr+'.pickle'), 'rb')
        color = pickle.load(pickle_color)
        print 'color file exists'
        return color

    claimRate = read_in()
    ##brandList = claimRate['brand_code'].drop_duplicates().tolist()
    brandList = TG_BRAND_CODE
   
    color = pd.DataFrame(columns=['brand_code','component_code','color_code'])
   ## compntList = set_compntList(cateUsr)
    for brand in brandList:
        
        compntList = claimRate[(claimRate['production_month'] == monthUsr) & \
                         (claimRate['brand_code'] == brand)]\
                         ['service_component_code'].drop_duplicates().tolist()

        for compnt in compntList:
           
            ## ---------------------  EXTREMELY SLOWWWW---------------------  ##
            compntBsl = baseLineCal(claimRate, brand, compnt)
            
            compntLine = compntLineCal(claimRate, monthUsr, brand, compnt)
            compnt_sir = compntLine['SIR'].tolist()
            baseline_up = compntBsl['std_SIR+'].tolist()
            baseline_low = compntBsl['std_SIR-'].tolist()
            
            ## get length of dataframe
            length = len(compnt_sir)
            i = 0
            while i < length:
                
                up = baseline_up[i]
                low = baseline_low[i]
                sir = compnt_sir[i]
                colorFlag = 2
                
                if sir > up:
                    colorCode = 0
                    colorFlag = 0
                    break
                elif sir < low:
                    colorCode = 1
                    colorFlag = 1

                elif sir >= low:
                    pass
                i += 1

            if colorFlag == 2:
                colorCode = 2
            newLine = pd.DataFrame([[brand,compnt,colorCode]], \
                        columns=['brand_code','component_code','color_code'])
            color = color.append(newLine)
            
            ##print color
            ## ------------------------------------------------------- ##    

    pickle_color = open(('color_'+monthUsr+'_'+cateUsr+'.pickle'),'wb')
    pickle.dump(color, pickle_color)
    pickle_color.close()
    
    return color 
    
def set_prodList():
    yearList = list()    
    claimRate = c_a.read_org_claim()
   # print claimRate, 'thsi is claim rate'
    prodList = claimRate['production_month']\
                   .drop_duplicates().tolist()
    for prod in prodList:
        year = prod.year
        month = prod.month
        month_year = str(month) + '-' + str(year)
        yearList.append(month_year)
    #print yearList,'this is yearList'
    return yearList



#def data_plot(brand_code, compnt_code):
def data_plot(product_month, brand_code, compnt_code):
    claimRate = read_in()
 
    compntBsl = baseLineCal(claimRate, brand_code, compnt_code)
    compntLine = compntLineCal(claimRate, product_month, brand_code, compnt_code)
    print ' ***********This is component Line *************'
    print compntLine
    print '------------ end of component line ---------------'

    print ' ***********This is Baseline Line *************'
    print compntBsl
    print '------------ end of Baseline line ---------------'
    fig, ax = plt.subplots(1, 1)
    ax.set_title('Cumulative Customer Claim Rate of %s in %s (%s)' \
                 %(compnt_code, brand_code, product_month))
    
    compntBsl.plot(ax = ax, x = 'period',y = 'avg_SIR')
    compntBsl.plot(ax = ax, x = 'period',y = 'std_SIR+', style = 'k--')
    compntBsl.plot(ax = ax, x = 'period',y = 'std_SIR-', style = 'k--')
    compntLine.plot(ax = ax, x = 'period',y = 'SIR', kind = 'scatter'\
                    , color = 'red', alpha = 0.6)
    ax.set_xlabel('Period(s) from Selected Production Month')
    ax.set_ylabel('Cumulative Customer Claim Rate')
    plt.show()


            
        
    
