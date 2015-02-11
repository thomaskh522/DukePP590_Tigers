from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import xlrd #MISSION CRITICAL

###DATA FILES (ex File1.txt) need to be in last folder mentioned in the main_dir pathway on code line 16
### PLEASE NOTE THAT READING EXCEL FILE REQUIRES XLRD, WHICH MAY NOT BE A CANOPY DEFAULT, USE PACKAGE MANAGER
###This can be run with a CSV of the ID excel sheet, line codes 18, 84-93 need to be activated
### THE CSV FILE IS ALSO IN OUR REPO named "IDS.csv"
### The default is to use the excel file (code starts at line 16 and then again at line 95)

### The final DataFrames are df_csv (made using csv file) and df_excel (made using excel file, which is default)


main_dir = "C:\Users\Kyle\Documents\NSOE_semester_4\Big_Data\Data_Files\CER_Electricity_Revised_March_2012\DATA/"
excel_file = "SME and Residential allocations.xlsx"
#csv_file = "IDS.csv" 

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
paths3 = [main_dir + v for v in os.listdir(main_dir) if v.startswith("File")]
lists = [pd.read_table(v, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing, skiprows = 6000000, nrows = 1500000) for v in paths3]
dftotal = pd.concat(lists, ignore_index = True)

#seperating hours from days-------------------------
hours = dftotal['date'] % 100
days = dftotal['date'] // 100
dftotal['days'] = days
dftotal['hours'] = hours
#del dftotal.date

#####CLEANING DATA####----------------------------------------------------------
#drop pure duplicates-----------------------------------------
dftotal = dftotal.drop_duplicates()
#looking for duplicated (mostly unhelpful)
dupid = dftotal.panid.duplicated() #not useful, IDs are going to be repeated
dupdate = dftotal.date.duplicated() #dates are duplicated as expected
dupkwh = dftotal.kwh.duplicated() #not really useful... kwh could be repeated

#looking at duplicated dates----------------------------------
dftotal[dupdate]
df2dup = dftotal[['date','kwh']].duplicated()

#look for missing data (there appears to be no missing data in these rows)------
nankwh = dftotal.kwh.isnull()
dftotal[nankwh]

nanpanid = dftotal.panid.isnull()
dftotal[nanpanid]

nandate = dftotal.date.isnull()
dftotal[nandate]



###Day light savings###--------------------------------------------------------------
dftotal[dftotal.days == 452] #not in data
dftotal[dftotal.days == 669] #not in data
dftotal[dftotal.days == 298] #in data

###IMPORTING AND MERGING ID DATA###---------------------------------------------
#CAN USE CSV METHOD OR EXCEL METHOD, DEFAULT RUNS EXCEL


#CSV METHOD-------------------------------------------------
#ids = pd.read_csv(main_dir + csv_file)
#id2 = ids[ids.Code == 3]
#id3 = ids.drop(id2.index)
#id3.columns = ['panid', 'code', 'tariff', 'stim', 'SME']
#df_final = pd.merge(dftotal, id3, how = 'outer')
#fourtynine = df_final[df_final.hours == 49] #id hour 49
#df_final2 = df_final.drop(fourtynine.index) #drops hour 49
#fifty = df_final2[df_final2.hours == 50] #id hour 50
#df_csv = df_final2.drop(fifty.index) #drop hour 50
#df_csv #final dataframe

#Working with excel sheet-----------------------------------------------------
exl = pd.read_excel(main_dir + excel_file, parse_cols = "A:E")
exl2 = exl[exl.Code == 3]
exl3 = exl.drop(exl2.index)
exl3.columns = ['panid', 'code', 'tariff', 'stim', 'SME']
df_xl = pd.merge(dftotal, exl3, how = "outer")
frtn = df_xl[df_xl.hours == 49]
no_frtn = df_xl.drop(frtn.index)
fty = no_frtn[no_frtn.hours == 50]
df_excel = no_frtn.drop(fty.index)
