from __future__ import division
from pandas import Series, DataFrame
from scipy.stats import ttest_ind
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import xlrd
import pytz 
import time
import matplotlib.pyplot as plt

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
root = main_dir + "\CER Electricity Data\CER Data\\"
excel_file = "\SME and Residential allocations.xlsx"
time_data = main_dir + "\CER Electricity Data\CER Data\\timeseries_correction.csv"

#import, iterating through a loop
paths3 = [os.path.join(root,v) for v in os.listdir(root) if v.startswith("File")]
dftotal = pd.concat([pd.read_table(v, names = ['panid', 'date', 'kwh'], sep = " ", nrows = 2000000) for v in paths3]) #Reads in 2,000,0000 rows of CER data
times = pd.read_csv(time_data, usecols = [2,3,4,5,6,9,10], parse_dates = [0]) #reads in time series data
###Day light savings###--------------------------------------------------------
#Splits up the date function into a day and hour columns, then renames the columns to match for common columns to merge on
hours = dftotal['date'] % 100
days = dftotal['date'] // 100
dftotal['day_cer'] = days
dftotal['hour_cer'] = hours

###IMPORTING AND MERGING ID DATA###---------------------------------------------
exl = pd.read_excel(root + excel_file, parse_cols = "A:E") #Brings in SME worksheet columns A-E
exl.columns = ['panid', 'code', 'tariff', 'stim', 'SME'] #renames columns
del exl['SME'] #delete SME column
excel = exl[exl.code == 1] #Only shows where Code is equal to 1 (Could possible remove the dropping Code 3 code)
idx = excel['stim'].isin(['1', 'E']) #Provides Boolean Index that is True for rows where stim is equal to 1 or E
excel = excel[idx] #Drops all values except those identified as True in idx code
tar = excel['tariff'].isin(['A', 'E']) #Same only for tarriff column equals to A and E
excel = excel[tar] #Drops all values except those ID'd as True in tar code

#MERGING DATA#
df = pd.merge(dftotal, excel, on = 'panid') #merges on Tarriff designation and CER data on panid column--SOMEHOW end up with more rows
del df['date'] #delete obsolete date column

#merges on both hour and day_cer columns.  Do this to avoid addition of rows to account for daylight savings time additional hours
df = pd.merge(df, times, on = ['hour_cer', 'day_cer']) 
#day and hour_cer cols no longer needed after merge
del df['hour_cer']
del df['day_cer']

#sorts by panid, then day, then hour but date is messed up
df.sort(['panid','day', 'hour'], inplace = True)

# DAILY AGGREGATION ------------------------------------------------------------
grp = df.groupby(['year', 'month', 'day', 'panid', 'tariff']) 
agg = grp['kwh'].sum()

# reset the index (multilevel at the moment)
agg = agg.reset_index() # drop the multi-index
grp1 = agg.groupby(['year', 'month', 'day', 'tariff'])#was date

## split up treatment/control
trt = {(k[0], k[1], k[2]): agg.kwh[v].values for k, v in grp1.groups.iteritems() if k[3] == 'A'}
ctrl = {(k[0], k[1], k[2]): agg.kwh[v].values for k, v in grp1.groups.iteritems() if k[3] == 'E'}
keys = ctrl.keys()

#make more efficent data Frames
#provides dataframes with pval and tstat for each month
tdf = DataFrame([(k, np.abs(ttest_ind(trt[k], ctrl[k], equal_var = False)[0])) for k in keys], columns = ['date', 'tstat'])
pdf = DataFrame([(k, np.abs(ttest_ind(trt[k], ctrl[k], equal_var = False)[1])) for k in keys], columns = ['date', 'pval'])
#puts pvals and tstats into one dataframe and then sorts by date
t_p = pd.merge(tdf, pdf)
t_p.sort(['date'], inplace = True)
t_p.reset_index(inplace = True, drop = True)

##plots two graphs on same plot with hor and vert lines and title
#Graphs 'tstat' column from dataframe t_p
fig1 = plt.figure()
p1 = fig1.add_subplot(2,1,1)
p1.plot(t_p['tstat']) 
p1.axvline(171, color = 'g', linestyle = '--')
p1.axhline(2, color = 'r', linestyle = '--')
plt.show()
p1.set_title("Daily T Stats")

p2 = fig1.add_subplot(2,1,2)
p2.plot(t_p['pval']) 
p2.axvline(171, color = 'g', linestyle = '--')
p2.axhline(.05, color = 'r', linestyle = '--')
p2.set_title("Daily P Values")

##MONTHLY AGGREGATION-----------------------------------------------------------
grp2 = df.groupby(['year', 'month', 'panid', 'tariff']) 
agg2 = grp2['kwh'].sum()

# reset the index (multilevel at the moment)
agg2 = agg2.reset_index() # drop the multi-index
grp3 = agg2.groupby(['year', 'month', 'tariff'])#was date

## split up treatment/control
trt2 = {(k[0], k[1]): agg2.kwh[v].values for k, v in grp3.groups.iteritems() if k[2] == 'A'}
ctrl2 = {(k[0], k[1]): agg2.kwh[v].values for k, v in grp3.groups.iteritems() if k[2] == 'E'}
keys2 = ctrl2.keys()

#make more efficent data Frames
#provides dataframes with pval and tstat for each month
tdf2 = DataFrame([(k, np.abs(ttest_ind(trt2[k], ctrl2[k], equal_var = False)[0])) for k in keys2], columns = ['date', 'tstat'])
pdf2 = DataFrame([(k, np.abs(ttest_ind(trt2[k], ctrl2[k], equal_var = False)[1])) for k in keys2], columns = ['date', 'pval'])
#puts pvals and tstats into one dataframe and then sorts by date
t_p2 = pd.merge(tdf2, pdf2)
t_p2.sort(['date'], inplace = True)
t_p2.reset_index(inplace = True, drop = True)

##plots two graphs on same plot with hor and vert lines and title
#Graphs 'tstat' column from dataframe t_p
fig2 = plt.figure()
p3 = fig2.add_subplot(2,1,1)
p3.plot(t_p2['tstat']) 
p3.axvline(6, color = 'g', linestyle = '--')
p3.axhline(2, color = 'r', linestyle = '--')
p3.set_title("Monthly T Stats")

p4 = fig2.add_subplot(2,1,2)
p4.plot(t_p2['pval']) 
p4.axvline(6, color = 'g', linestyle = '--')
p4.axhline(.05, color = 'r', linestyle = '--')
p4.set_title("Monthly P Values")
