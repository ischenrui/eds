
#  author   ：feng
#  time     ：2018/1/25
#  function : 数据库抽象功能函数
import pymysql

from algorithm.base.config import POOL


class dbutil:

    def getDics(self,sql,params=None):
        conn = POOL.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        if params is None:
            cursor.execute(sql)
        else :
            cursor.execute(sql, params)
        result = cursor.fetchall()
        conn.close()
        return result

    def getTuples(self,sql,params=None):
        conn = POOL.connection()
        cursor = conn.cursor()
        if params is None:
            cursor.execute(sql)
        else :
            cursor.execute(sql, params)
        result = cursor.fetchall()
        conn.close()
        return result

    def exe_sql(self,sql,params=None):
        conn = POOL.connection()
        cursor = conn.cursor()
        if params is None:
            r=cursor.execute(sql)
        else :
            r=cursor.execute(sql, params)
        conn.commit()
        conn.close()
        return r