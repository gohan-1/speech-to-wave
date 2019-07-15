#!/usr/bin/env python
import pandas as pd
from pandas import DataFrame as f
from pandas import Series as s
import matplotlib.pyplot as plt

fig=plt.figure()
zomato=pd.read_csv("zomato.csv")
for i in range(1,3):
 fig.add_subplot(2,2,i)
 #plt.subplot(2,2,i)
 zomato1=zomato[zomato['Price range']==i]
 zomato1=zomato1[zomato1['Country Code']==1]
 zomatoT= zomato1.sort_values('Aggregate rating',ascending=0).head(10)

 plt.bar(x=zomatoT['Restaurant Name'],height=zomatoT['Aggregate rating'],width=0.4)


plt.show()
