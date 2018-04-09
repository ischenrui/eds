import pymysql

class DataUtils(object):
    def __init__(self, host='localhost', port = 3306,
                 user='root', passwd ='zjl112', db='ceshi', charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset

    def conn(self):
        """
        连接数据库,返回连接对象
        :return: conn
        """
        return pymysql.connect(host=self.host, port=self.port,
                               user=self.user, passwd=self.passwd,
                               db=self.db, charset=self.charset)

    def select_one(self, select_sql):
        """
        返回下一行查询到的数据
        :param select_sql: 查询语句
        :return: tuple
        """
        conn = self.conn()
        cursor = conn.cursor()
        cursor.execute(select_sql)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def select_all(self, select_sql):
        """
        返回所有查询行
        :param select_sql:
        :return: tuple
        """
        conn = self.conn()
        cursor = conn.cursor()
        cursor.execute(select_sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def insert_many(self, insert_sql, list_sql):
        """
        向表中插入多条数据
        :return:
        """
        conn = self.conn()
        cursor = conn.cursor()
        cursor.executemany(insert_sql, list_sql)
        conn.commit()
        cursor.close()
        conn.close()

    def insert_one(self, insert_sql):
        """
        向表中插入一条数据
        :return:
        """
        conn = self.conn()
        cursor = conn.cursor()
        cursor.execute(insert_sql)
        conn.commit()
        cursor.close()
        conn.close()
