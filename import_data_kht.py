from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "C:\Users\Kyle\Documents\NSOE_semester_4\Big_Data\Data_Files\CER_Electricity_Revised_March_2012\DATA/"
#file1 = "\File1.txt"
#file2 = "\File2.txt"
#file3 = "\File3.txt"
#file4 = "\File4.txt"
#file5 = "\File5.txt"
#file6 = "\File6.txt"
#missing = [".", "NA", "NULL", "-", "999999999"]

#import data one file at a time for the lulz
#df1 = pd.read_table(main_dir + file1, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing, skiprows = 6000000, nrows = 1500000)
#df2 = pd.read_table(main_dir + file2, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing, skiprows = 6000000, nrows = 1500000)
#df3 = pd.read_table(main_dir + file3, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing, skiprows = 6000000, nrows = 1500000)
#df4 = pd.read_table(main_dir + file4, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing, skiprows = 6000000, nrows = 1500000)
#df5 = pd.read_table(main_dir + file5, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing, skiprows = 6000000, nrows = 1500000)
#df6 = pd.read_table(main_dir + file6, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing, skiprows = 6000000, nrows = 1500000)
#dfm = pd.concat([df1,df2,df3,df4,df5,df6], ignore_index=True)
#del([df1,df2,df3,df4,df5,df6])

#import attempt 2, iterating through a loop
paths3 = [main_dir + v for v in os.listdir(main_dir)]
lists = [pd.read_table(v, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing, skiprows = 6000000, nrows = 1500000) for v in paths3]
dftotal = pd.concat(lists, ignore_index = True)

#seperating hours from days
hours = dftotal['date'] % 100
days = dftotal['date'] // 100
dftotal['days'] = days
dftotal['hours'] = hours
del dftotal.date

#drop pure duplicates
dftotal = dftotal.drop_duplicates()
dftotal

#looking for duplicated
dupid = dftotal.panid.duplicated() #not useful, IDs are going to be repeated
dupdate = dftotal.date.duplicated() #dates are duplicated... need to address this
dupkwh = dftotal.kwh.duplicated() #not really useful... kwh could be repeated
#looking at duplicated dates
dftotal[dupdate]
df2dup = dftotal[['date','kwh']].duplicated()

#look for missing data (there appears to be no missing data in these rows)
nankwh = dftotal.kwh.isnull()
dftotal[nankwh]

nanpanid = dftotal.panid.isnull()
dftotal[nanpanid]

nandate = dftotal.date.isnull()
dftotal[nandate]