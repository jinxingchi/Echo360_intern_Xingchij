import os
import sys, getopt
import xlrd
import pickle
import pandas as pd
import numpy as np
import scipy as sp
import math as mt
from scipy.stats import poisson
from scipy.stats import exponweib as ew
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt


## Set directory
path = os.getcwd()
os.chdir(path)
print "#############################  System Info  #############################"
print 'The current directory is', path



## Declare variables
brandUsr = 'KAD'
prodIdUsr = '582'
compntUsr = '331'
prodMthUsr = '2015-08-01'
partSqUsr = 1
periodUsr = 4
predictPeriodUsr = 12
print "brand: " + brandUsr
print "product ID: " + prodIdUsr
print "component ID: " + compntUsr
print "production month: " + prodMthUsr
print "period of prediction" + str(predictPeriodUsr)
print "number of month after the target production month: " + str(periodUsr)

EXCEL_CLAIM = 'claimset_1607.xlsx'
EXCEL_VOLUME = 'total_vol_1607.xlsx'
EXCEL_SHIP = 'shipment_1607.xlsx'
EXCEL_FILTER_KEYS = ['brand', 'product_code', \
                     'production_month', 'service_complete_date', \
                     'service_component_code', 'part_sequence', \
                     'shipped_month', 'shipped_size', 'volume']
print "claim file: " + EXCEL_CLAIM
print "production volume file: " + EXCEL_VOLUME

SALE_POISSMEAN = 2

LIST_VOLUME_DIST = [0.000000, 0.067349, 0.178649, 0.226664, 0.208625, \
                    0.152382, 0.091418, 0.045810, 0.019354, 0.006934, \
                    0.002114, 0.000550, 0.000000]

## Read in data from excel
if ((EXCEL_VOLUME.replace('.xlsx', '.pickle')) in (os.listdir(path))):
    pk_rawVolData = open((EXCEL_VOLUME.replace('.xlsx', '.pickle')), 'rb')
    df_rawVolData = pickle.load(pk_rawVolData)
    print 'Raw volume file exists'
else:
    df_rawVolData = pd.read_excel(EXCEL_VOLUME)
    pk_rawVolData = open((EXCEL_VOLUME.replace('.xlsx', '.pickle')),'wb')
    pickle.dump(df_rawVolData, pk_rawVolData)
    pk_rawVolData.close()

if ((EXCEL_CLAIM.replace('.xlsx', '.pickle')) in (os.listdir(path))):
    pk_rawClaimData = open((EXCEL_CLAIM.replace('.xlsx', '.pickle')), 'rb')
    df_rawClaimData = pickle.load(pk_rawClaimData)
    print 'Raw claim file exists'
else:
    df_rawClaimData = pd.read_excel(EXCEL_CLAIM)
    pk_rawClaimData = open((EXCEL_CLAIM.replace('.xlsx', '.pickle')),'wb')
    pickle.dump(df_rawClaimData, pk_rawClaimData)
    pk_rawClaimData.close()        

if ((EXCEL_SHIP.replace('.xlsx', '.pickle')) in (os.listdir(path))):
    pk_rawShipData = open((EXCEL_SHIP.replace('.xlsx', '.pickle')), 'rb')
    df_rawShipData = pickle.load(pk_rawShipData)
    print 'Raw shipment file exists'
else:
    df_rawShipData = pd.read_excel(EXCEL_SHIP)
    pk_rawShipData = open((EXCEL_SHIP.replace('.xlsx', '.pickle')),'wb')
    pickle.dump(df_rawShipData, pk_rawShipData)
    pk_rawShipData.close()
print "#############################  System Info  #############################"



## Pre-process data
df_rawClaimData[EXCEL_FILTER_KEYS[0]] = df_rawClaimData[EXCEL_FILTER_KEYS[0]].astype(str)
df_rawClaimData[EXCEL_FILTER_KEYS[1]] = df_rawClaimData[EXCEL_FILTER_KEYS[1]].astype(int)
df_claim = df_rawClaimData[(df_rawClaimData[EXCEL_FILTER_KEYS[0]] == brandUsr)]
df_claim[EXCEL_FILTER_KEYS[1]] = df_claim[EXCEL_FILTER_KEYS[1]].astype(str)
df_claim = df_claim[(df_claim[EXCEL_FILTER_KEYS[1]] == prodIdUsr)]
df_claim[EXCEL_FILTER_KEYS[4]] = df_claim[EXCEL_FILTER_KEYS[4]].astype(str)
df_claim = df_claim[(df_claim[EXCEL_FILTER_KEYS[4]] == compntUsr)]
df_claim = df_claim[(df_claim[EXCEL_FILTER_KEYS[5]] == partSqUsr)]

df_claim[EXCEL_FILTER_KEYS[2]] = pd.to_datetime(df_claim[EXCEL_FILTER_KEYS[2]])
df_claim[EXCEL_FILTER_KEYS[2]] = df_claim[EXCEL_FILTER_KEYS[2]].apply(lambda x: x.replace(day = 1))
df_claim[EXCEL_FILTER_KEYS[3]] = pd.to_datetime(df_claim[EXCEL_FILTER_KEYS[3]])
df_claim[EXCEL_FILTER_KEYS[3]] = df_claim[EXCEL_FILTER_KEYS[3]].apply(lambda x: x.replace(day = 1))


df_rawVolData[EXCEL_FILTER_KEYS[0]] = df_rawVolData[EXCEL_FILTER_KEYS[0]].astype(str)
df_rawVolData[EXCEL_FILTER_KEYS[1]] = df_rawVolData[EXCEL_FILTER_KEYS[1]].astype(int)
df_vol = df_rawVolData[(df_rawVolData[EXCEL_FILTER_KEYS[0]] == brandUsr)]
df_vol[EXCEL_FILTER_KEYS[1]] = df_vol[EXCEL_FILTER_KEYS[1]].astype(str)
df_vol = df_vol[(df_vol[EXCEL_FILTER_KEYS[1]] == prodIdUsr)]

df_vol[EXCEL_FILTER_KEYS[2]] = pd.to_datetime(df_vol[EXCEL_FILTER_KEYS[2]])
df_vol[EXCEL_FILTER_KEYS[2]] = df_vol[EXCEL_FILTER_KEYS[2]].apply(lambda x: x.replace(day = 1))

df_rawShipData[EXCEL_FILTER_KEYS[1]] = df_rawShipData[EXCEL_FILTER_KEYS[1]].astype(str)
df_ship = df_rawShipData[(df_rawShipData[EXCEL_FILTER_KEYS[1]] == prodIdUsr)]
df_ship[EXCEL_FILTER_KEYS[2]] = pd.to_datetime(df_ship[EXCEL_FILTER_KEYS[2]])
df_ship[EXCEL_FILTER_KEYS[2]] = df_ship[EXCEL_FILTER_KEYS[2]].apply(lambda x: x.replace(day = 1))
df_ship[EXCEL_FILTER_KEYS[6]] = pd.to_datetime(df_ship[EXCEL_FILTER_KEYS[6]])
df_ship[EXCEL_FILTER_KEYS[6]] = df_ship[EXCEL_FILTER_KEYS[6]].apply(lambda x: x.replace(day = 1))



## Weibull fitting using linear least square estimation
def weibullFit(weibX, weibY):
    x = np.array(weibX)
    y = np.array(weibY)

##    A = np.vstack([x, np.ones(len(x))]).T
##    m, c = np.linalg.lstsq(A, y)[0]
##
##    beta = m
##    ita = mt.exp(-(c/m))
##    weibPara = (beta, ita)
##
##    print weibPara
##    return weibPara

    def fn(x, k, b):
        return k*x + b

    k, b = curve_fit(fn, x, y)[0]
    print (k,b)
    beta = k
    ita = mt.exp(-(b/k))
    weibPara = (beta, ita)

    print weibPara
    return weibPara

## Collect claim data --> Naveda Table
list_prodMth = df_claim[EXCEL_FILTER_KEYS[2]].drop_duplicates().tolist()
endMth = pd.to_datetime(prodMthUsr) + pd.DateOffset(months = periodUsr)
startMth = endMth - pd.DateOffset(months = 12)
if startMth not in list_prodMth:
    startMth = list_prodMth[0]

list_prodMth = list_prodMth[list_prodMth.index(startMth):(list_prodMth.index(endMth)+1)]
list_claimMth = list_prodMth

naveda_Matrix = [[0]*len(list_claimMth) for i in range(len(list_prodMth))]
i = 0
for prodMth in list_prodMth:
    j = 0
    for claimMth in list_claimMth:
        if claimMth <= prodMth:
            naveda_Matrix[i][j] = 0
        else:
            naveda_Matrix[i][j] = df_claim[(df_claim[EXCEL_FILTER_KEYS[2]] == prodMth) & \
                                           (df_claim[EXCEL_FILTER_KEYS[3]] == claimMth)]\
                                           [EXCEL_FILTER_KEYS[5]].count()
        j = j + 1
    i = i + 1

print "############################# Naveda Matrix #############################"
print "Naveda table:"
print np.matrix(naveda_Matrix)
print "############################# Naveda Matrix #############################"



## Calculate sales distribution --> Sales Volume Table
def saleMthCal(prodMth):
    df_shipTemp = df_ship[(df_ship[EXCEL_FILTER_KEYS[2]] == pd.to_datetime(prodMth))]
    shipSum = df_shipTemp.sum(axis = 0)[EXCEL_FILTER_KEYS[7]]
    mthShip = df_shipTemp[EXCEL_FILTER_KEYS[7]].tolist()

    prodVol = sum(df_vol[(df_vol[EXCEL_FILTER_KEYS[2]] == pd.to_datetime(prodMth))]\
                  [EXCEL_FILTER_KEYS[8]].tolist())
    
    mthTemp = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    salePercent = [0] * len(mthTemp)
    for month in mthTemp:
        mthTemp[mthTemp.index(month)] = poisson.cdf(month,mu = SALE_POISSMEAN, loc = 0)
    for cdf in mthTemp:
        if mthTemp.index(cdf) == 0:
            salePercent[mthTemp.index(cdf)] = mthTemp[mthTemp.index(cdf)]
        if mthTemp.index(cdf) > 0:
            salePercent[mthTemp.index(cdf)] = mthTemp[mthTemp.index(cdf)] - \
                                          mthTemp[mthTemp.index(cdf) - 1]
    
    mthSale_Matrix = [[0]*len(salePercent) for i in range(len(mthShip))]
    for shipment in mthShip:
        i = mthShip.index(shipment)
        j = 0
        while j < len(salePercent):
            if i > j:
                pass
            else:
                mthSale_Matrix[i][j] = (shipment * salePercent[j-i])
            j = j + 1
   
    saleSum = sum([sum(x) for x in mthSale_Matrix])

    saleMth = [sum(x) for x in zip(*mthSale_Matrix)]
    saleMthPercent = [x/shipSum for x in saleMth]

    mthlySale = [prodVol * x for x in saleMthPercent]

    return mthlySale

saleMthAll_Matrix = [0] * len(list_prodMth)
for month in list_prodMth:
    i = list_prodMth.index(month)
    saleMthAll_Matrix[i] = saleMthCal(month)[0:len(list_prodMth)]

    temp = [0] * len(saleMthAll_Matrix[i])
    temp[i:] = saleMthAll_Matrix[i][0:len(saleMthAll_Matrix[i])-i]
    temp = [round(x,0) for x in temp]
    saleMthAll_Matrix[i] = temp
print saleMthAll_Matrix
saleMthAllSum = [sum(x) for x in zip(*saleMthAll_Matrix)]
print "########################## Monthly sales volume #########################"
print "Monthly sales:"
print np.matrix(saleMthAllSum).T



## form life distribution data 
def navedaDiagSum(naveda_Table):
    i = len(naveda_Table)
    nvDiagSum = [0] * i
    for m in range(i):
        nvDiagSum[m] = sum([naveda_Table[n][n+m] for n in range(i-m)])
    
    return nvDiagSum

claimMth = navedaDiagSum(naveda_Matrix)
print "Claims:"
print np.matrix(claimMth).T

def corrRiskCal(riskSeed):
    unCorrRisk = [sum(riskSeed[0:i+1]) \
                  for i in list(reversed(range(len(riskSeed))))]

    corrRisk = [0] * len(unCorrRisk)
    for risk in unCorrRisk:
        i = unCorrRisk.index(risk)
        if i == 0:
            corrRisk[i] = unCorrRisk[i]
        else:
            risk = risk - sum(claimMth[0:i]) + \
                   sum([sum(naveda_Matrix[len(corrRisk)-k-1][(len(corrRisk))-k-1:]) \
                   for k in range(i)])
            corrRisk[i] = risk

    return corrRisk

corrRisk = corrRiskCal(saleMthAllSum)
print "Corrected risk set:"
print np.matrix(corrRisk).T
print "########################## Monthly sales volume #########################"



## perform weibull fitting
def weibPredict():
    hazard = [claimMth[i]/corrRisk[i] for i in range(len(corrRisk))]
    
    cumulHazard = [0] * len(hazard)
    for hzd in hazard:
        i = hazard.index(hzd)
        cumulHazard[i] = sum(hazard[0:i+1])
    
    reliability = [mt.exp(-x) for x in cumulHazard]
    
    claimCDF = [1-x for x in reliability]
    
    weibY = [mt.log(-mt.log(1-x)) for x in claimCDF[1:]]
    weibX = [mt.log(x) for x in range(len(claimCDF))[1:]]
    
    weibPara = weibullFit(weibX, weibY)
    weibCDF = [ew.cdf(i, a = 1, c = weibPara[0], scale = weibPara[1]) \
                      for i in range(predictPeriodUsr)]
    print weibCDF
    
    claimPercent = [0] * len(weibCDF)
    for cdf in weibCDF:
        i = weibCDF.index(cdf)
        if i == 0:
            claimPercent[i] = cdf
        if i > 0:
            claimPercent[i] = cdf - weibCDF[i - 1]

##    claimPercent = weibPDF
    print claimPercent
    return claimPercent


def failurePredict():
    saleProdMth = saleMthCal(prodMthUsr)
    print sum(saleProdMth)
    claimPercent = weibPredict()

    failPredict = [0] * len(claimPercent)
    for percent in claimPercent:
        i = claimPercent.index(percent)
        failPredict[i] = claimPercent[i] * sum(saleProdMth[0:(len(saleProdMth)-i-1)])

    return failPredict
claimPredict = failurePredict()
claimPredict = [0.5*x for x in claimPredict]


df_realClaim = df_claim[(df_claim[EXCEL_FILTER_KEYS[2]] == pd.to_datetime(prodMthUsr))]  
EXCEL_FILTER_KEYS = ['brand', 'product_code', \
                     'production_month', 'service_complete_date', \
                     'service_component_code', 'part_sequence', \
                     'shipped_month', 'shipped_size', 'volume']
list_realClaimMth = [pd.to_datetime(prodMthUsr)+pd.DateOffset(months = i) \
                     for i in range(12)]
realClaim = [0] * len(list_realClaimMth)
for month in list_realClaimMth:
    i = list_realClaimMth.index(month)
    print month
    realClaim[i] = df_realClaim[(df_realClaim[EXCEL_FILTER_KEYS[3]] == month)]\
                                           [EXCEL_FILTER_KEYS[5]].count()
print realClaim


plt.plot(range(12),realClaim)
plt.plot(range(12),claimPredict)
plt.show()
