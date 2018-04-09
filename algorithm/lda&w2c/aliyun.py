from databaseUtils import *
from sklearn.externals import joblib
db = DataUtils(host='120.78.201.159', db='eds', passwd='zdf.0126')

def get_fields():
    sql = """select author_id, theme from theme_year"""
    result = db.select_all(sql)
    fieldsDict = {}
    for tuple in result:
        author_id = tuple[0]
        theme = tuple[1]
        if(author_id in fieldsDict and theme not in fieldsDict[author_id]):
            fieldsDict[author_id] = fieldsDict[author_id] + ','+theme
        elif(author_id in fieldsDict and theme in fieldsDict[author_id]):
            pass
        else:
            fieldsDict[author_id] =  theme
    joblib.dump(fieldsDict, 'fieldsDict.pkl')
    return  fieldsDict

def insert_fiels(fieldsDict):
    conn = db.conn()
    cursor = conn.cursor()
    for id, fields in fieldsDict.items():
        try:
            sql = """update teacher set fields = '%s' where id = %s"""%(fields, id)
            cursor.execute(sql)
        except:
            print(fields)
    conn.commit()
    cursor.close()
    conn.close()


fieldsDict = get_fields()
# print(fieldsDict)
print('===================')
# fieldsDict = joblib.load('fieldsDict.pkl')
# print(len(fieldsDict))
insert_fiels(fieldsDict)

# print(fieldsDict[28645])
