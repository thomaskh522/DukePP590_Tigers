from __future__ import division
import pandas as pd
import numpy as np
import os

main_dir = '/Users/Fei/Desktop/Data/task4/'

# CHANGE WORKING DIRECTORY (wd)
os.chdir(main_dir)
from logit_functions import *

# IMPORT DATA ------------
df = pd.read_csv(main_dir + 'task_4_kwh_w_dummies_wide.csv')
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
        
        print(logit_results.summary())
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


##### section 2
logit_results, df_logit = do_logit(df_pretrial, 'C', '4', add_D=None, mc=False)
df_logit['p_hat'] = logit_results.predict()
df_logit['trt'] = 0 + (df_logit['tariff'] == 'C')
df_logit['w']=np.sqrt(df_logit['trt']/df_logit['p_hat']+(1-df_logit['trt'])/(1-df_logit['p_hat']))

df_w = df_logit[['ID', 'trt', 'w']]

#### section 3
from fe_functions import *
df1 = pd.read_csv(main_dir + 'task_4_kwh_long.csv')
df2 = pd.merge(df1,df_logit)