

n=raw_input("enter the whole string")
b=raw_input("enter the word you want to search")

l1=n.split()
for i in range(len(l1)):
    if l1[i]==b:
     print i+1
