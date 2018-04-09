from databaseUtils import *
from sklearn.externals import joblib
from time import time
db = DataUtils()

def institution_dumup():
    """
    存储所有学院的一个列表
    :return: list
    """
    result = db.select_all('select institution from teacher')
    institutionLst = []
    for i in range(0, len(result)):
        if(result[i][0] not in institutionLst):
            institutionLst.append(result[i][0])
    joblib.dump(institutionLst, 'institution.pkl')
    return institutionLst

def teacher_dump(institutionLst):
    """
    把专家id对应学院存储起来
    :return: dict
    """
    teacherDict = {}
    # institutionLst = joblib.load('institution.pkl')
    for institution in institutionLst:
        result = db.select_all('select id from teacher where institution= "%s" ' % institution )
        teacherLst = []
        for i in range(0, len(result)):
            teacherLst.append(result[i][0])
        teacherDict[institution] = teacherLst
    joblib.dump(teacherDict, 'teacherInstitution.pkl')
    return teacherDict

def insert_doclda(teacherDict):
    """
    把数据重新整理,存放在表(doclda)里
    :return:
    """
    # teacherDict = joblib.load('teacherInstitution.pkl')
    for key, value in teacherDict.items():
        for id in value:
            result = db.select_all('select * from paper where author_id = %d' % id)
            if(result):
                list_sql = []
                for i in range(0, len(result)):
                    data = (result[i][0], id, result[i][14],key, result[i][3], result[i][9], result[i][5])
                    list_sql.append(data)
                insert_sql = 'insert into doclda (id_paper, id_teacher, md5_paper, institution_teacher, abstract_paper, keyword_paper, year_paper) ' \
                             'values(%s, %s, %s, %s, %s, %s, %s) '
                db.insert_many(insert_sql, list_sql)


def main():
    # teacher表不变的情况下, 如果只有paper表变化,仅需要重新运行insert_doclda即可
    s1 = time()
    institutionLst = institution_dumup()
    s2 = time()
    print('time_2 = ', s2 - s1)
    teacherDict = teacher_dump(institutionLst)
    s3 = time()
    print('time_3 = ', s3 - s2)
    insert_doclda(teacherDict)
    print('time_4 = ', time() - s1)

def test():
    # sql = """INSERT INTO doclda VALUES (200010, 318321, '56d92b313bad0d19eaa7b6d99323a146', '18484', '电气与电子工程学院', '实施双语教学，是我国新世纪提高高等学校英语教育质量的举措之一，双语教学肩负着专业能力和英语能力培养的双重任务,本文结合笔者多年电路理论课程双语教学的实践经验，探讨双语教学的基本规律，总结双语教学模式，论述影响双语教学效果的关键因素，介绍了电路理论课程实施双语教学的一些具体做法和使用英语教材的体会。', '探索实践,双语教学,电路课程,教学改革,电路理论', '2007', null);"""
    # db.insert_one(sql)
    pass

if __name__ == '__main__':
    start = time()
    main()
    print('time used ->', time() - start)
    # pass
