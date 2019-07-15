
#importing packages

import pandas as pd
import numpy as np
from pandas import Series as s

#reading json file

today=pd.read_json("t.json",lines=True)
yesterday=pd.read_json("y.json",lines=True)

print "1st question answer"
#merging the two files with same urlh
print"\n"
merged=pd.merge(today,yesterday,how="inner",on="urlh")
print "number of items with overlapping"
print merged.shape[0]
#print today.columns

print"\n"
#print yesterday.columns
print "2nd question"

print"\n"
print "Items which having diifernce in thire today and yesterdays availabe price  "
difference=merged['available_price_x']-merged['available_price_y']
#print differnce.columns
print difference[difference>0]
print"\n"
print "3rd question"

print"\n"
print "unique categories count"

print"\n"
#print today.columns
print "today's count","\t",len(today['category'].unique())
print"\n"
print "yesterday's count","\t",len(yesterday['category'].unique())

print"\n"
print "4th question"

merged1=pd.merge(today,yesterday,how="outer",on="category")
print "number of distinct categories",merged1.shape[0]

#print today.columns

print"\n"
print "5th question"

print"\n"

for i in today['category'].unique():
 x=today[today['category']==i]
 cnt=0
 for j in x['subcategory'].unique():
  cnt=len(x['subcategory']==j)
  print i+ ' > '+j + ':' + str(cnt) 

print"\n"
print "6th question"
today[today['mrp']==0]=np.nan
today[today['mrp'].isna()]=np.nan
print"\n"
print today['mrp']

print "all the types are float"
print type(today['mrp'])
