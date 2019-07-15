import requests
import json
from pprint import pprint
import csv



header = { "user_key": "e5709e436b3bfb075430f566ecca27e9"}
def city(chn):

      
 locationUrlFromLatLong = "https://developers.zomato.com/api/v2.1/cities?q="+str(chn)


 response = requests.get(locationUrlFromLatLong,headers=header)

 fdw= open('f1.txt', 'a')
 pprint(response.json())
 fdw.write(str(response.json())+'\n')
 
with open('project.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        city(row)



