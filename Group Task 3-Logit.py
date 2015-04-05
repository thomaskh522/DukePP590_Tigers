from __future__ import division
from pandas import Series, DataFrame
from scipy.stats import ttest_ind
from datetime import datetime, timedelta
from dateutil import parser
import pandas as pd
import numpy as np
import os
import xlrd
import pytz 
import time
import matplotlib.pyplot as plt
import statsmodels.api as sm

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
root = main_dir + "\Python\Data\\"

df = pd.read_csv(root + "allocation_subsamp.csv", header = 0)

# Cuts off the extra variables leaving only tariff and stimulus
df['tarstim'] = df['tariff'] + df['stimulus']

# Number 1-Creates separate vectors for each control or treatment group
dfEE = df[df['tarstim']=='EE']
dfA1 = df[df['tarstim']=='A1']
dfA3 = df[df['tarstim']=='A3']
dfB1 = df[df['tarstim']=='B1']
dfB3 = df[df['tarstim']=='B3']

np.random.seed(1789)  #Number 2
#Number 3-Takes samples from each trt and ctrl group
sampEE = np.random.choice(dfEE['ID'], 300, replace = False)
sampA1 = np.random.choice(dfA1['ID'], 150, replace = False)
sampA3 = np.random.choice(dfA3['ID'], 150, replace = False)
sampB1 = np.random.choice(dfB1['ID'], 50, replace = False)
sampB3 = np.random.choice(dfB3['ID'], 50, replace = False)

#Number 4-creates dataframe out of samples
ids = sampEE.tolist() + sampA1.tolist() + sampA3.tolist()+ sampB1.tolist() + sampB3.tolist()
ids2 = DataFrame(ids, columns = ['ID'])

#Number 5-Import consumption data
consump = pd.read_csv(root + 'kwh_redux_pretrial.csv')
#Number 6-Merging with ids dataframe of samples
df2 = pd.merge(ids2, consump)
#Number 7-aggregate monthly consumption
grp_month = df2.groupby(['year', 'month', 'ID']) 
agg2 = grp_month['kwh'].sum()
agg2 = agg2.reset_index()
#Number 8-Add 'kwh_month' column and pivot
agg2['kwh_month'] = 'kwh_' + agg2['month'].apply(str)
agg2_piv = agg2.pivot('ID', 'kwh_month', 'kwh')
agg2_piv.reset_index(inplace = True) # this makes panid its own variable
agg2_piv.columns.name = None

#Number 9-Merge with allocation dataset
df_total = pd.merge(agg2_piv, df)

