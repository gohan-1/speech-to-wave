
import functools 
import operator  
  
def convertTuple(tup): 
    str =  ' '.join(tup) 
    return str
from itertools import permutations  
l1=list()
with open(r"C:\Users\ADMIN\Downloads\Microsoft.SkypeApp_kzf8qxf38zg5c!App\All\domains.txt", 'r') as infile:
    for lines in infile:
        words=lines.split("\n")[0]
        #perm=permutations(lines.strip())
        l1.append(words)

perm=permutations(l1)
for i in perm:
    #print(type(i))
    str = convertTuple(i) 
    print(str)