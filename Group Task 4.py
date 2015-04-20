from __future__ import division
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import os
import statsmodels.api as sm

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
root = main_dir + "\Python\Data\\"

# CHANGE WORKING DIRECTORY (wd)
os.chdir(root)
from logit_functions import *
from fe_functions import *

# IMPORT DATA ------------
df = pd.read_csv(root + 'task_4_kwh_w_dummies_wide.csv')
df = df.dropna(axis=0, how='any')

# GET TARIFFS ------------
tariffs = [v for v in pd.unique(df['tariff']) if v != 'E']
stimuli = [v for v in pd.unique(df['stimulus']) if v != 'E']
tariffs.sort()
stimuli.sort()

# RUN LOGIT
drop = [v for v in df.columns if v.startswith("kwh_2010")]
df_pretrial = df.drop(drop, axis=1)

for i in tariffs:
    for j in stimuli:
        # dummy vars must start with "D_" and consumption vars with "kwh_"
        logit_results, df_logit = do_logit(df_pretrial, i, j, add_D=None, mc=False)
        
# QUICK MEANS COMPARISON WITH T-TEST BY HAND----------
# create means
grp = df_logit.groupby('tariff')
df_mean = grp.mean().transpose()
df_mean.C - df_mean.E

# do a t-test "by hand"
df_s = grp.std().transpose()
df_n = grp.count().transpose().mean()
top = df_mean['C'] - df_mean['E']
bottom = np.sqrt(df_s['C']**2/df_n['C'] + df_s['E']**2/df_n['E'])
tstats = top/bottom
sig = tstats[np.abs(tstats) > 2]
sig.name = 't-stats'

###########################################
#Section 2
###########################################

logit_results, df_logit = do_logit(df_pretrial, 'C', '4', add_D=None, mc=False)
df_logit['p_hat'] = logit_results.predict()
df_logit['trt'] = 0 + (df_logit['tariff'] == 'C')
df_logit['w']=np.sqrt(df_logit['trt']/df_logit['p_hat']+(1-df_logit['trt'])/(1-df_logit['p_hat']))

df_w = df_logit[['ID', 'trt', 'w']]

df_w

#### section 3

df1 = pd.read_csv(root + 'task_4_kwh_long.csv')
df2 = pd.merge(df1,df_logit)

##creating necessary variables
#treatment and trial interaction var
trial = [v for v in df.columns if v.startswith("kwh_2010")]
pretrial = [v for v in df.columns if v.startswith("kwh_2009")]
df2['trial'] = 

#log of consumption
df2['log_kwh'] = (df2['kwh'] + 1).apply(np.log)

#ym
df2['mo_str'] = np.array(["0" + str(v) if v < 10 else str(v) for v in df2['month']])
df2['ym'] = df2['year'].apply(str) + "_" + df2['mo_str']

p = (df2['ym'] !='2009_08') & (df2['ym'] !='2009_09')&(df2['ym'] !='2009_10') &(df2['ym'] !='2009_11')&(df2['ym'] !='2009_12') 
df2['p'] = 0 + p 

df2['TP'] = df2['trt'] * df2['p']


y = df2['log_kwh']
P = df2['p']
TP = df2['TP']
w = df2['w']
mu = pd.get_dummies(df2['ym'], prefix = 'ym').iloc[:, 1:-1]

y = DataFrame(df2['log_kwh'])
P = DataFrame(df2['p'])
TP = DataFrame(df2['TP'])
w = DataFrame(df2['w'])
mu = DataFrame(pd.get_dummies(df2['ym'], prefix = 'ym').iloc[:, 1:-1])


X = pd.concat([TP, P, mu], axis = 1)

ids = df2['ID']
y = demean(y, ids)
X = demean(X, ids)

##Without Weights
fe_model = sm.OLS(y, X)
fe_results = fe_model.fit()
print(fe_results.summary())

##With Weights
y = DataFrame(df2['log_kwh'])
P = DataFrame(df2['p'])
TP = DataFrame(df2['TP'])
w = DataFrame(df2['w'])
mu = DataFrame(pd.get_dummies(df2['ym'], prefix = 'ym').iloc[:, 1:-1])
X = pd.concat([TP, P, mu], axis = 1)
y = y*w
X = X.T
nms = X.columns.values

#X = np.array([x*w for k, x in X.iteritems()])
#X = X.T
#X = DataFrame(X, columns = nms)

fe_w_model = sm.OLS(y, X)
fe_w_results = fe_w_model.fit()
print(fe_w_results.summary())




