from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

###IMPORTANT!!!! DATA FILES (ex File1.txt) need to be in last folder mentioned in the main_dir pathway on code line 13!!!#####
### IMPORTANT!!! there is also a new_dir pathway on code line 72 this must be changed for the merging to work
### IMPOTANT!!! there is a "need" variable on line 73, this must be csv file of the ids, WE CREATED THIS FILE AND SAVED AS CSV
### THE CSV FILE IS ALSO IN OUR REPO named "IDS.csv"


main_dir = "C:\Users\Kyle\Documents\NSOE_semester_4\Big_Data\Data_Files\CER_Electricity_Revised_March_2012\DATA/"
#file1 = "\File1.txt"
#file2 = "\File2.txt"
#file3 = "\File3.txt"
#file4 = "\File4.txt"
#file5 = "\File5.txt"
#file6 = "\File6.txt"
missing = [".", "NA", "NULL", "-", "999999999"]

#import data one file at a time
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
#del dftotal.date

#drop pure duplicates
dftotal = dftotal.drop_duplicates()


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

#Day light savings
dftotal[dftotal.days == 452] #not in data
dftotal[dftotal.days == 669] #not in data
dftotal[dftotal.days == 298] #in data

#import merge data
new_dir = "C:\Users\Kyle\Documents\NSOE_semester_4\Big_Data\A1/"
need = "SME and Residential allocations"
ids = pd.read_csv(new_dir + need)
id2 = ids[ids.Code == 3]
id3 = ids.drop(id2.index)
id3.columns = ['panid', 'code', 'tariff', 'stim', 'SME']
df_final = pd.merge(dftotal, id3, how = 'outer')
fourtynine = df_final[df_final.hours == 49]
df_final2 = df_final.drop(fourtynine.index)
fifty = df_final2[df_final2.hours == 50]
df_final3 = df_final2.drop(fifty.index)
df_final3