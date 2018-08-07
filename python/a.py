import datetime

now = datetime.datetime.now()
t1 = now.second
print (t1)
now = datetime.datetime.now()
t2 = now.second
print (t2)
t3 = t2-t1
print (t3)
