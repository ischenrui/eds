
from teacher.util.mysql import *

mysql=Mysql()
list=mysql.select()
t=0
f=open('text.txt','w+')
for l in list:
    it={}
    it['id_paper_left']=l[1]
    it['id_paper_right']=l[2]
    item=mysql.selectItem(it)
    le=len(item)
    t+=1
    # print(le)
    for i in range(1,le):
        print(i)
        temp=str(item[i][0])+'\n'
        f.write(temp)
