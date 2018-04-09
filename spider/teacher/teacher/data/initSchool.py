
from teacher.items import *
from teacher.util.mysql import *

f=open("school.txt")
mysql=Mysql()
school = SchoolItem()

while 1:
    line = f.readline()
    if not line:
        break
    if line[0]=='1':
        str=line.split(' ')
        school['school']=str[1].strip()
    elif len(line)>1:
        str = line.split('：')
        school['adpart']=str[0].strip()
        try:
            links=str[1].split("&&&")
        except:
            print('err'+line)
        for link in links:
            school['url']=link.strip()
            mysql.insertSchool(school)