from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import xlrd #MISSION CRITICAL
import pytz
from datetime import datetime, timedelta
import time

main_dir = "C:\Users\Kyle\Documents\Big_Data\CER_Data"
root = main_dir + "/raw"
excel_file = "SME and Residential allocations.xlsx"
time_data = main_dir + "/timeseries_correction.csv"

#missing = [".", "NA", "NULL", "-", "999999999"]

#import attempt 2, iterating through a loop
paths3 = [os.path.join(root,v) for v in os.listdir(root) if v.startswith("File")]
dftotal = pd.concat([pd.read_table(v, names = ['panid', 'date', 'kwh'], sep = " ") for v in paths3])
times = pd.read_csv(time_data, usecols = [2,3,4,5,6,9,10])
###Day light savings###--------------------------------------------------------

hours = dftotal['date'] % 100
days = dftotal['date'] // 100
dftotal['day_cer'] = days
dftotal['hour_cer'] = hours
#ad_hour = times['hour_cer'][:48]

###IMPORTING AND MERGING ID DATA###---------------------------------------------
exl = pd.read_excel(main_dir + "/raw/" + excel_file, parse_cols = "A:E")
exl2 = exl[exl.Code == 3]
exl3 = exl.drop(exl2.index)
exl3.columns = ['panid', 'code', 'tariff', 'stim', 'SME']
del exl3['SME']
excel = exl3[exl3.code == 1]
idx = excel['stim'].isin(['1', 'E'])
excel = excel[idx]
tar = excel['tariff'].isin(['A', 'E'])
excel = excel[tar]

#MERGING DATA#
df = pd.merge(dftotal, excel, on = 'panid')
del df['date']
#del df['day_cer']
#del df['minute']
#del df[
df = pd.merge(df, times, on = ['hour_cer', 'day_cer'])
del df['hour_cer']
del df['day_cer']

df.sort(['panid','day', 'hour'], inplace = True)

#df = pd.groupby(df, by=['panid', 'day', 'hour'])

#STATS#-------------------------------------------------------------------------
from scipy.stats import ttest_ind

trt = df['kwh'][df.tariff == 'E']
crtl = df['kwh'][df.tariff == 'A']

t, p = ttest_ind(trt, crtl, equal_var = False)


### Time Series
# DAILY AGGREGATION --------------------
grp = df.groupby(['month', 'year', 'panid', 'tariff']) #was date
agg = grp['kwh'].sum()


# reset the index (multilevel at the moment)
agg = agg.reset_index() # drop the multi-index
grp = agg.groupby(['month', 'year', 'tariff'])#was date

## split up treatment/control
trt = {k[0]: agg.kwh[v].values for k, v in grp.groups.iteritems() if k[2] == 'A'} # get set of all treatments by date (1 by day, 2 by month)
ctrl = {k[0]: agg.kwh[v].values for k, v in grp.groups.iteritems() if k[2] == 'E'} # get set of all controls by date (1 by day 2 by month)
keys = ctrl.keys()



#make more efficent data Frames
tdf = DataFrame([(k, np.abs(ttest_ind(trt[k], ctrl[k], equal_var = False)[0])) for k in keys], columns = ['date', 'tstat'])
pdf = DataFrame([(k, np.abs(ttest_ind(trt[k], ctrl[k], equal_var = False)[1])) for k in keys], columns = ['date', 'pval'])
t_p = pd.merge(tdf, pdf)
t_p.sort(['date'], inplace = True)
t_p.reset_index(inplace = True, drop = True)

#PLOTTING DATA# ----------------------------------------------------------------
import matplotlib.pyplot as plt

fig1 = plt.figure()
p1 = fig1.add_subplot(2,1,1)
p1.plot(t_p['tstat']) 
p1.axhline(2, color = 'r', linestyle = '--')
plt.show()
p1.set_title("Daily T Stats")

p2 = fig1.add_subplot(2,1,2)
p2.plot(t_p['pval']) 
p2.axhline(.05, color = 'r', linestyle = '--')
p2.set_title("Daily P Values")