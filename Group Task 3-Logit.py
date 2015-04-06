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
#fixes the ordering of the months--For example, creates 01 for Jan which is diff from 1
agg2['mo_str'] = ['0' + str(v) if v < 10 else str(v) for v in agg2['month']]
agg2['kwh_month'] = 'kwh_' + agg2['mo_str'].apply(str)
agg2_piv = agg2.pivot('ID', 'kwh_month', 'kwh')
agg2_piv.reset_index(inplace = True) # this makes panid its own variable
agg2_piv.columns.name = None

#Number 9-Merge with allocation dataset
df_total = pd.merge(agg2_piv, df)

#Number 10-Logit Model

df_logit = pd.get_dummies(df_total, columns = ['tarstim'])

kwh_cols = [v for v in df_logit.columns.values if v.startswith('kwh')]

A1_cols = ['tarstim_A1'] + kwh_cols
A3_cols = ['tarstim_A3'] + kwh_cols
B1_cols = ['tarstim_B1'] + kwh_cols
B3_cols = ['tarstim_B3'] + kwh_cols

##Set up Y, X
#y is treatment or control
y = df_logit['tarstim_EE']
# X is the variables that we want to use as Betas and adds constant
X1 = df_logit[A1_cols]
X1 = sm.add_constant(X1)

X2 = df_logit[A3_cols]
X2 = sm.add_constant(X2)

X3 = df_logit[B1_cols]
X3 = sm.add_constant(X3)

X4 = df_logit[B3_cols]
X4 = sm.add_constant(X4)

##logit--Logit is used to determine the relationships between the variables prior to running regression
#results show no relationship between the variables and the assignments
logit_model1 = sm.Logit(y, X1)
logit_results1 = logit_model1.fit()
print(logit_results1.summary())

logit_model2 = sm.Logit(y, X2)
logit_results2 = logit_model2.fit()
print(logit_results2.summary())

logit_model3 = sm.Logit(y, X3)
logit_results3 = logit_model3.fit()
print(logit_results3.summary())

logit_model4 = sm.Logit(y, X4)
logit_results4 = logit_model4.fit()
print(logit_results4.summary())


