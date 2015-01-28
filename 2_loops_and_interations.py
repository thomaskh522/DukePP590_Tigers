from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os


#code goes in GitHub directory, and data goes in main directory-----------------
main_dir = "C:\Users\Kyle\Desktop\data"
git_dir = "C:\Users\Kyle\Documents\GitHub\PubPol590"
csv_file = "sample_data_clean.csv"

#FOR LOOPS: allows iteration through a lsit/object------------------------------
df = pd.read_csv(os.path.join(main_dir, csv_file))

list1 = range(10,15)
list2 = ['a','b','c']
list3 = [1, 'a', True]

## iterating over elements (for loops)
#loops in side new work area, it wont be visible unless you make it visible with print command
for v in list1:
    print(v)

for v in list2:
    print(v)
    
for v in list3:
    print(v, type(v)) #you can use , to print multiple objects on the line

##populating empty lists-------------------------------------------------------
list1 #is all int
list4 = []
list5 = []

for v in list1:
    v2 = v**2
    list4.extend([v2]) #only accepts 'list' object
    list5.append(v2) #appends whatever obj as is
    
[v**2 for v in list1] #shorthand for for loops, [] make it a list, 
list6 = [v**2 < 144 for v in list1] #this fails because cannot squate a string

## iterating using enumeration
list7 =[ [i,v/2] for i, v in enumerate(list1)] #returns index (i) and v/2 for each i and v in list1
list8 =[ [i,float(v)/2] for i, v in enumerate(list1)]


## ITERATE THROUGH A SERIES-----------------------------------------------------
s1 = df['consump']
[v > 2 for v in s1]
[[i,v] for i, v in s1.iteritems()] 

#ITERATE THROUGH A DATAFRAME----------------------------------------------------
[v for v in df]
[df[v] for v in df]
[[i,v] for i, v in df.iteritems()]
    

    
