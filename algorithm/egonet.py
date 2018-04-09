

import json
from algorithm.base import dbs

print('导出数据')
sql='SELECT paper.id,paper.author_id,paper.author,teacher.name,teacher.institution from paper  JOIN  teacher  on paper.author_id=teacher.id'
list=dbs.getDics(sql)
sql = 'SELECT id,name,school,institution from  teacher'
teacher = dbs.getDics(sql)
print('开始关联')
for t in teacher:
    t['name']=t['name'].replace(' ','')
egoNet={}
for l in list:
    id=str(l['author_id'])
    try:
        author=json.loads(l['author'])
    except:
        print(l)
    name=l['name'].replace(' ','')
    for a in author:
        if len(a)>=1 and name!=a['name']:
            find = False
            for t in teacher:
                if a['name'] ==t['name'] and (len(a['org'])==0 or a['org'].find(t['school'])>=0):
                    find=True
                    key=id+'_'+str(t['id'])+'_'+a['name']
                    if key in egoNet.keys():
                        if l['id'] not in egoNet[key]:
                            egoNet[key].append(l['id'])
                    else:
                        egoNet[key]=[]
                        egoNet[key].append(l['id'])
            if find==False:
                key=id+'_-1_'+a['name']+'*'+a['org']
                if key in egoNet.keys():
                    if l['id'] not in egoNet[key]:
                        egoNet[key].append(l['id'])
                else:
                    egoNet[key] = []
                    egoNet[key].append(l['id'])


for e in egoNet:
    id=e.split('_')
    try:
        parm=(id[0],id[1],id[2],len(egoNet[e]))
    except:
        print(e)
    sql='insert into ego_network values(null,%s,%s,%s,%s)'
    dbs.exe_sql(sql,parm)
