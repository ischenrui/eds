from mysql import Mysql
import json
import pymysql.cursors
# 连接数据库
class Mysql(object):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Cr648546845',
        db='projectdata',
        charset='utf8'
)
# 获取游标
    cursor = connect.cursor()
    # 查询专家编号
    def SltTid(self):
        sql = "SELECT id,name,school FROM papaer_teacherlist "
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def SltTdid(self):
        sql = "SELECT id FROM teacherdata "
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def SltTinsitution(self,id):
        sql = "SELECT institution FROM teacherdata WHERE id=%s"
        params = (id)
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def DP(self,pid):
        sql = "DELETE FROM papaer_teacherlist WHERE id=%s"
        params = (pid)
        self.cursor.execute(sql,params)
        self.connect.commit()
        print("删除pid成功")

    def DTd(self,pid):
        sql = "DELETE FROM teacherdata WHERE id=%s"
        params = (pid)
        self.cursor.execute(sql,params)
        self.connect.commit()
        print("删除pid成功")

    # 插入论文
    def InsertT(self, id,name,school,institution):
        sql = "INSERT INTO teacher_new VALUES(%s,%s,%s,%s)"
        params = (id,name,school,institution)
        self.cursor.execute(sql, params)
        self.connect.commit()


if __name__ == '__main__':
    sql = Mysql()

    # ------读取文件--------
    # file = open("F:/Myproject/Python/TeacherInfo/chenrui/eds/data/news_tensite_xml.dat",encoding='gb18030',errors='ignore')
    #
    # # while 1:
    # # lines = file.readlines(1000)
    # # # if not lines:
    # #     # break
    # # for line in lines:
    # #     print(line)
    #
    # linenum = 0
    # for line in file:
    #     linenum+=1
    #     x = linenum%6
    #     print(x)
    #     print(line)
    #     print('-'*100)
# -----------根据papaer_teacherlist清理teacherdata------------
    # arr = sql.SltTid()
    # ptlist = [x[0] for x in arr]
    # # print(ptlist)
    #
    # arr = sql.SltTdid()
    # tlist = [x[0] for x in arr]
    # # print(tlist)
    #
    # list3 = list(set(tlist)-set(ptlist))
    # for node in list3:
    #     print(node)
    #     sql.DTd(node)


#-----------根据insert teacher_new------------
    # tlist = sql.SltTid()
    # for tnode in tlist:
    #     tid = tnode[0]
    #     name = tnode[1]
    #     school = tnode[2]
    #     institution = sql.SltTinsitution(tid)[0]
    #     sql.InsertT(tid,name,school,institution)


    pass