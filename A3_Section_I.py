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


main_dir = "/Users/amitpalsingh/Documents/Duke Academics/Spring 2015/PubPol 590 Big Data/00 Data/"
allo = "data_all/09_allocation_subsamp.csv"
redux = "data_all/09_kwh_redux_pretrial.csv"

df = pd.read_csv(main_dir + allo, header = 0)

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
consump = pd.read_csv(main_dir + redux)
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

#LOGIT STUFF

#Generate Dummy Variables
df_dum = pd.get_dummies(df_total, columns = ['tarstim'])
#df_dum.drop(['tarstim_EE'], axis = 1, inplace = True) may not be necessary

#trial 1
kwh_cols = [v for v in df_dum.columns.values if v.startswith('kwh')]
tarstims = ['tarstim_A1', 'tarstim_A3', 'tarstim_B1', 'tarstim_B3', 'tarstim_EE']

A1_cols = ['tarstim_A1'] + kwh_cols
A3_cols = ['tarstim_A3'] + kwh_cols
B1_cols = ['tarstim_B1'] + kwh_cols

B3_cols = ['tarstim_B3'] + kwh_cols

##Set up Y, X
#y is treatment or control
y = df_dum['tarstim_EE']


"""MAJOR FIXES REQUIRED. RESULTS DID NOT WORK OUT OF THE BOX. DATASTRUCTURES INCORRECT."""
# X is the variables that we want to use as Betas and adds constant
X1 = df_dum[A1_cols].ix[(df_dum.tarstim_A1==1) | (df_dum.tarstim_EE==1), 1:]
X1 = sm.add_constant(X1)

X2 = df_dum[A3_cols].ix[(df_dum.tarstim_A3==1) | (df_dum.tarstim_EE==1), 1:]
X2 = sm.add_constant(X2)

X3 = df_dum[B1_cols].ix[(df_dum.tarstim_B1==1) | (df_dum.tarstim_EE==1), 1:]
X3 = sm.add_constant(X3)

X4 = df_dum[B3_cols].ix[(df_dum.tarstim_B3==1) | (df_dum.tarstim_EE==1), 1:]
X4 = sm.add_constant(X4)

"""It is not sufficient to just tag values. The data in the model should ONLY include the rows
of data relevant to what is being modeled. Furthermore, you should not include on the right
hand side any variables that label something as "treatment" when the left hand side is a value for
"control". This leads to perfect prediction/singularity."""

logit_model1 = sm.Logit(y[(df_dum.tarstim_A1==1) | (df_dum.tarstim_EE==1)], X1)
logit_results1 = logit_model1.fit()

logit_model2 = sm.Logit(y[(df_dum.tarstim_A3==1) | (df_dum.tarstim_EE==1)], X2)
logit_results2 = logit_model2.fit()

logit_model3 = sm.Logit(y[(df_dum.tarstim_B1==1) | (df_dum.tarstim_EE==1)], X3)
logit_results3 = logit_model3.fit()

logit_model4 = sm.Logit(y[(df_dum.tarstim_B3==1) | (df_dum.tarstim_EE==1)], X4)
logit_results4 = logit_model4.fit()

print(logit_results1.summary())
print(logit_results2.summary())
print(logit_results3.summary())
print(logit_results4.summary())
