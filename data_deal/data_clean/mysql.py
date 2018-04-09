import pymysql.cursors
# 连接数据库
class Mysql(object):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Cr648546845',
        db='eds',
        charset='utf8'
)
# 获取游标
    cursor = connect.cursor()

    # 插入专家
    def InsertTeacher(self, name,position,title,school,institution,phone,eduexp,email,pic,homepage,author_id):
        sql = "INSERT INTO teacher VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())"
        params = (name,position,title,school,institution,phone,eduexp,email,pic,homepage,author_id)
        self.cursor.execute(sql, params)
        self.connect.commit()

    # 插入theme_year
    def InsertTheme(self, author_id, paper_md5, year, theme):
        sql = "INSERT INTO theme_year VALUES(NULL,%s,%s,%s,%s)"
        params = (author_id, paper_md5, year, theme)
        self.cursor.execute(sql, params)
        self.connect.commit()

    # 插入radar
    def InsertRadar(self, author_id, paper_num, citation, h_index,G_index,sociability):
        sql = "INSERT INTO radar VALUES(NULL,%s,%s,%s,%s,%s,%s)"
        params = (author_id, paper_num, citation, h_index,G_index,sociability)
        self.cursor.execute(sql, params)
        self.connect.commit()

    # 插入ego_network
    def InsertEgonetwork(self, author_id, coauthor,w):
        sql = "INSERT INTO ego_network VALUES(NULL,%s,%s,%s)"
        params = (author_id, coauthor,w)
        self.cursor.execute(sql, params)
        self.connect.commit()