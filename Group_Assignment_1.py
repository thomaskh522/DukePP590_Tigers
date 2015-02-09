#Initialize Script
from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
git_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis\GitHub\PubPol590"

missing = [".", "NA", 'NULL', '', '999999999']
txt_file1 = "\CER Electricity Data\CER Data\File1.txt"
txt_file2 = "\CER Electricity Data\CER Data\File2.txt"
txt_file3 = "\CER Electricity Data\CER Data\File3.txt"
txt_file4 = "\CER Electricity Data\CER Data\File4.txt"
txt_file5 = "\CER Electricity Data\CER Data\File5.txt"
txt_file6 = "\CER Electricity Data\CER Data\File6.txt"

df1 = pd.read_table(main_dir + txt_file1, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing)
df2 = pd.read_table(main_dir + txt_file2, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing)
df3 = pd.read_table(main_dir + txt_file3, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing)
df4 = pd.read_table(main_dir + txt_file4, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing)
df5 = pd.read_table(main_dir + txt_file5, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing)
df6 = pd.read_table(main_dir + txt_file6, names = ['panid', 'date', 'kwh'], sep = " ", na_values = missing)

df_full = pd.concat([df1, df2, df3, df4, df5, df6] , ignore_index = True)

