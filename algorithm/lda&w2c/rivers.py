from sklearn.externals import joblib
from databaseUtils import *
import time
import traceback
db = DataUtils()

def id_teacher_extract():
    """
    无重复提取doclda里面的老师id
    并存储到idTeacher.pkl里
    :return: list
    """
    idLst = []
    sql = """select distinct id_teacher from doclda"""
    result = db.select_all(sql)
    for i in range(0, len(result)):
        idLst.append(result[i][0])
    joblib.dump(idLst, 'idTeacher.pkl')
    print(idLst)

def insert_theme_year():
    """
    向theme_year表里面插入数据
    :return:
    """
    conn = db.conn()
    cursor = conn.cursor()
    idLst = joblib.load('idTeacher.pkl')
    for id_teacher in idLst:
        start = time.time()
        sql_select = "select institution_teacher, id_teacher, id_paper, md5_paper,  year_paper, topic_paper from doclda where id_teacher = %s order by id_teacher" % id_teacher
        result = db.select_all(sql_select)
        try:
            for i in range(0, len(result)):
                index = int(result[i][5]) % 6
                theme = result[i][0] + '_' + str(index)
                sql_insert = "insert into theme_year(author_id, paper_id, paper_md5, year, theme) " \
                             "values ('%s', '%s', '%s', '%s', '%s')" % (result[i][1], result[i][2], result[i][3], result[i][4], theme)
                cursor.execute(sql_insert)
        except:
            pass
        print('time -> ', time.time() - start)
    conn.commit()
    cursor.close()
    conn.close()

def tag_extract(institution_teacher):
    sql = """select topicid_institution, tag_word from topiclda where institution_teacher = '%s'""" % institution_teacher
    result = db.select_all(sql)
    tagDict = {}
    for tuple in result:
        id = tuple[0]
        tag = tuple[1]
        tagDict[id] = tag
    return tagDict

def tag_insert(institution_teacher):
    tagDict = tag_extract(institution_teacher)
    sql_select = "select id_teacher, id_paper, md5_paper,  year_paper, topic_paper from doclda where institution_teacher = '%s'" % institution_teacher
    result = db.select_all(sql_select)
    conn = db.conn()
    cursor = conn.cursor()

    for i in range(0, len(result)):
        id = result[i][4]
        theme = tagDict[id]
        year = result[i][3].strip()
        sql_insert = "insert into theme_year(author_id, paper_id, paper_md5, year, theme) " \
                     "values ('%s', '%s', '%s', '%s', '%s')" % (
                     result[i][0], result[i][1], result[i][2], year, theme)
        try:
            if(len(year) == 4 and year != '被引量:'):
                cursor.execute(sql_insert)
            else:
                print(year)
        except:
            traceback.print_exc()
    conn.commit()
    cursor.close()
    conn.close()

def main():
    # id_teacher_extract()
    # insert_theme_year()
    # institutionLst = joblib.load('institutionDoclda.pkl')
    institutionLst = ['计算机科学与工程学院']
    for institution in institutionLst:
        s1 = time.time()
        tag_insert(institution)
        print(institution, '->', time.time() - s1)

def test():
    institution = joblib.load('institutionDoclda.pkl')
    print(institution)
    print(len(institution))

if __name__ == '__main__':
    start = time.time()
    # test()
    main()
    print('time used = ', time.time() - start)