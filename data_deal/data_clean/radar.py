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
        sql = "SELECT id FROM teacher_add "
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def Sltpaper(self,id):
        sql = "SELECT id,cited_num,author FROM paper WHERE author_id=%s"
        params = (id)
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    # 插入radar表
    def Insertr(self, author_id,paper_sum ,paper_cite ,hindex ,gindex ,sociability):
        sql = "INSERT INTO radar VALUES(NULL,%s,%s,%s,%s,%s,%s)"
        params = (author_id,paper_sum ,paper_cite ,hindex ,gindex ,sociability)
        self.cursor.execute(sql, params)
        self.connect.commit()
if __name__ == '__main__':
    sql = Mysql()

    #--------radar表数值计算及插入--------------
    tlist = sql.SltTid()
    for tnode in tlist:
        tid = tnode[0]
        print(tid)
    #     tid = 20
        plist = sql.Sltpaper(tid)

        paper_sum = 0
        paper_cite = 0
        hindex = 0
        gindex = 0
        sociability = 0

        #--------paper_cite---------
        citelist = [x[1] for x in plist]
        citelist.sort(reverse=True)
        for citenode in citelist:
            paper_cite += citenode
            paper_sum += 1
            # print(paper_cite, paper_sum)
            if citenode>=paper_sum:hindex=paper_sum
            if paper_cite>paper_sum*paper_sum:gindex=paper_sum

        # print(citelist)
        # print(paper_cite,paper_sum,hindex,gindex)

        # --------paper_author---------
        coolist = []
        coonum = 0
        author_list = [x[2] for x in plist]
        for anode in author_list:
            # print(anode)
            try:
                authorjson = json.loads(anode)
                for author in authorjson:
                    if author:coolist.append(author['name'])
            except:print('json解析author出问题了')
        coonum = len(set(coolist))
        sociability = coonum

        print(paper_sum ,paper_cite ,hindex ,gindex ,sociability )
        sql.Insertr(tid,paper_sum ,paper_cite ,hindex ,gindex ,sociability)



    pass
