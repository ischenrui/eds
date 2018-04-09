from mysql import Mysql
import json
import pymysql.cursors
import uuid



# 连接数据库
class Mysql(object):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Cr648546845',
        db='sed',
        charset='utf8'
)
# 获取游标
    cursor = connect.cursor()
    # 查询专家编号
    def SltTid(self):
        sql = "SELECT id,name FROM teacher_add "
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def SltPaper(self):
        sql = "SELECT author_id FROM paper "
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def SltTdataid(self):
        sql = "SELECT id FROM teacherdata "
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def SltPauthor(self,id):
        sql = "SELECT author,paper_md5,id FROM paper WHERE author_id=%s"
        params = (id)
        self.cursor.execute(sql,params)
        return self.cursor.fetchall()

    def DPcr(self,pmd5):

        sql = "DELETE FROM paper_citeorref WHERE paper_md5=%s"
        params = (pmd5)
        self.cursor.execute(sql,params)
        self.connect.commit()
        print("删除pmd5成功")

    def DP(self,pid):

        sql = "DELETE FROM paper WHERE id=%s"
        params = (pid)
        self.cursor.execute(sql,params)
        self.connect.commit()
        print("删除pid成功")

    def uppaperauthor(self):
        sql = "SELECT id,author FROM paper "
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def UpdateAuthor(self, id,name):
        sql = "UPDATE paper SET author=%s where id=%s"
        params = (name,id)
        self.cursor.execute(sql, params)
        self.connect.commit()
        print("gengxing:::::",id)

    def SltPauthor1(self,id):
        sql = "SELECT id,name,abstract,keyword,author,author_id,paper_md5 FROM paper WHERE author_id=%s"
        params = (id)
        self.cursor.execute(sql,params)
        return self.cursor.fetchall()

    def SltTeacher(self,id):
        sql = "SELECT school,name FROM teacher_add WHERE id=%s"
        params = (id)
        self.cursor.execute(sql,params)
        return self.cursor.fetchone()

    def UpdatePtlist(self,id):
        sql = "UPDATE papaer_teacherlist SET search=0 where id=%s"
        params = (id)
        self.cursor.execute(sql, params)
        self.connect.commit()
        print("gengxing:::::", id)

    def Sltteacherdata(self):
        sql = "SELECT id,name,school,institution,email FROM teacherdata"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def Dlete(self,id):
        sql = "DELETE FROM teacherdata WHERE id=%s"
        params = (id)
        self.cursor.execute(sql, params)
        self.connect.commit()
        print("删除pid成功")

    def Dletetlis(self,id):
        sql = "DELETE FROM papaer_teacherlist WHERE id=%s"
        params = (id)
        self.cursor.execute(sql, params)
        self.connect.commit()
        print("删除pid成功")

def compareT(t1,t2):
    if t1[2]==t2[2]:
        if t1[3] == t2[3]:
            return True
        else:
            if (not t1[4] is None) and (t1[4] == t2[4]):
                return True
            else:
                return False
    else:
        return False

if __name__ == '__main__':
    sql = Mysql()


    Tid_list = sql.SltTid()
    for tidlist in Tid_list:
        tid = tidlist[0]
        tauthor = tidlist[1]

        plist = sql.SltPauthor1(tid)
        for paper in plist:
            pid = paper[0]
            name = paper[1]
            abstract = paper[2]
            keyword = paper[3]
            author = paper[4]
            author_id = paper[5]
            paper_md5 = paper[6]

            flag_kong = 0
            flag_shan = 0
            if name=="":flag_kong+=1
            elif len(name)<5:flag_kong+=1
            if abstract=="":flag_kong+=1
            elif len(abstract)<20:flag_shan = 1
            if keyword=="":flag_kong+=1
            if flag_kong>=2:flag_shan=1
            try:
                authorjson = json.loads(author)
                flag_name = 0
                for authornode in authorjson:
                    if authornode :
                        if authornode['name']==tauthor:
                            flag_name=1
                    elif not authornode:
                        flag_name=1
                if flag_name==0:flag_shan=1
            except:print(pid)

            if flag_shan==1:
                print("*" * 100)
                print(paper)
                print(author)
                print(tauthor)
                print('删除~')
                # print(flag_kong, flag_name)
                # sql.DPcr(paper_md5)
                sql.DP(pid)
    # #
    # # ----------删除authorlist中不存在author的papaer和cr--------------
    teacherlist = sql.SltTid()
    tidlist = [x[0] for x in teacherlist]

    paperlist = sql.SltPaper()
    pidlist = [x[0] for x in paperlist]

    dlist = list(set(pidlist)-set(tidlist))
    print(dlist)
    for dtid in dlist:
        tid = dtid
        plist = sql.SltPauthor1(tid)
        for paper in plist:
            pid = paper[0]

            print(paper)
            print(pid)
            # sql.DPcr(paper_md5)
            sql.DP(pid)
    # #
    # # ------------删除重名paper和cr-------------
    totol = 0
    sum = 0
    tlist = sql.SltTid()
    for tnode in tlist:
        tid = tnode[0]

    # tid = 1173
    #
        teacherinfo = sql.SltTeacher(tid)
        school = teacherinfo[0]
        name = teacherinfo[1]
        # print(school,name)

        paperlist = sql.SltPauthor(tid)
        for paper in paperlist:
            sum += 1
            author = paper[0]
            paper_md5 = paper[1]
            pid = paper[2]
            dflag = 0
            try:
                authorjson = json.loads(author)
                for author in authorjson:
                    if author and name==author['name']:
                        #----必须包含全部-----
                        if author['org'] == '' or author['org'].find(school)>-1:
                            # print(author['org'].find(school))
                            dflag = 1
                        else:print(school,author['org'])
                        #---包含部分词语就不删---
                        # s1 = school.replace('大学', '')
                        # s2 = author['org'].replace('大学', '')
                        # if author['org']=='' or len(s1)-len(set(s1)-set(s2))>1:
                        #     dflag = 1
                        # else:print(school,author['org'])
            except:
                print('json解析author出问题了')
            if dflag==0:
                # sql.DPcr(paper_md5)
                sql.DP(pid)
                totol+=1
            print(totol,sum,tid)

    print(totol)


    pass
