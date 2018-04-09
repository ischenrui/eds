from mysql import Mysql
import json
import pymysql.cursors
import re
import requests
import hashlib
import os
# 连接数据库

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root) #当前目录路径
        # print(dirs) #当前路径下所有子目录
        # print(files) #当前路径下所有非目录子文件
        return files

def getDomain(url):
    reg = r'^https?:\/\/([a-z0-9\-\.]+)[\/\?]?'
    m = re.match(reg, url)
    uri = m.groups()[0] if m else ''
    temp = uri[uri.rfind('.', 0, uri.rfind('.')) + 1:]
    index = url.index(temp) + len(temp)
    return url[0:index]

def getTeacherUrl(url,image_url):
    image_url = image_url.strip()
    domain=getDomain(url)
    if len(image_url) == 0:
        return ' '
    if image_url[0:4] == 'http':
        return image_url
    if image_url[0] == '/':
        return domain + image_url
    elif url[-1] == '/' and image_url[0] == '.':
        return url + image_url
    elif url[-1] == '/':
        index = url[0:-1].rfind('/')
        if index == -1:
            l = url + image_url
        else:
            l = domain + '/' + image_url
        return l
    else:
        index = url.rfind('/')
        return url[0:index + 1] + image_url

def dealHtml(html):
    if not html:return ""
    strInfo = html
    # html文本，使用正则去除标签
    strInfo = re.sub("<script[^>]*?>.*?</script>", "\r\n", strInfo)
    strInfo = re.sub("<style[^>]*?>.*?</style>", "\r\n", strInfo)
    strInfo = re.sub("<[^>]*>", "\r\n", strInfo)
    strInfo = strInfo.replace("&nbsp;", " ")
    strlist = strInfo.split('\r\n')
    out = ""
    for node in strlist:
        if len(node.strip()) > 0:
            out += node.strip()
            # out += node.strip() + '\n'
    return out

def readfile(fname):
    f1 = open(fname,encoding='UTF-8')
    doc = f1.read()
    list = doc.split('\n')
    return list

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

    def SltTeacher_new_id(self):
        sql = "SELECT id,name FROM papaer_teacherlist"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def SltTeacherdata(self):
        sql = "SELECT id,link,institution_url FROM teacherdata where id>15080"
        # params = (id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def UpdateTeacher_new_info(self, id,info):
        sql = "UPDATE teacher_new SET cleaninfo=%s where id=%s"
        params = (info,id)
        self.cursor.execute(sql, params)
        self.connect.commit()

    def UpdateTeacher(self,id,name):
        sql = "UPDATE teacher SET name=%s where author_id=%s"
        params = (name, id)
        self.cursor.execute(sql, params)
        self.connect.commit()

    def SltTeacherdata(self):
        sql = "SELECT id,title,email FROM eteacher"
        # params = (id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def sltimgurl(self):
        sql = "SELECT id,institution_url,image,link FROM teacherdata"
        # params = (id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def sltimgid(self):
        sql = "SELECT id FROM picinfo"
        # params = (id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

if __name__ == '__main__':
    sql = Mysql()

#----头像下载-----
    # imlist = sql.sltimgid()
    # imlist = [x[0] for x in imlist]
    #
    # list = sql.sltimgurl()
    # #
    # for sqllist in list:
    #     id = sqllist[0]
    #     if id not in imlist:
    #         print(id,'buzai')
    #
    #
    #         institution = sqllist[1]
    #         image_url = sqllist[2]
    #         link = sqllist[3]
    #
    #         homepage = getTeacherUrl(institution,link)
    #
    #
    #         try:
    #             imglist = image_url.split('-link-')
    #         except:
    #             print('imglist图片切割有问题')
    #         print(imglist)
    #         i = 1
    #         for imgurl in imglist:
    #             url = getTeacherUrl(homepage,imgurl)
    #         #     # print(id)
    #         #     print(id,url)
    #             try:
    #                 pic_url = url
    #                 req = requests.get(pic_url,timeout=3)
    #                 pic_md5 = hashlib.md5(pic_url.encode('utf - 8')).hexdigest()
    #                 # item['pic'] = pic_md5
    #                 fp = open("imgs//%s.jpg" % (str(id)+"-"+str(i)), 'wb')
    #                 fp.write(req.content)
    #                 fp.close()
    #             except:
    #                 print('url错误')
    #             i+=1


#-------拷贝信息到teacher---------
    # list = sql.SltTeacher_new_id()
    # for node in list:
    #     id = node[0]
    #     name = node[1]
    #     # email = node[2]
    #     print(id,name)
    #     sql.UpdateTeacher(id,name)
#----拼接homepage------

    # list = sql.SltTeacherdata()
    # for node in list:
    #     id = node[0]
    #     link = node[1]
    #     institutionurl = node[2]
    #     # print(id,link,institutionurl)
    #     url = getTeacherUrl(institutionurl,link)
    #     sql.UpdateTeacher(id,url)


#--------cleaninfo拷贝到teacher_new-----------
    # teacherlist = sql.SltTeacher_new_id()
    # tidlist = [x[0] for x in teacherlist]
    # for tid in tidlist:
    #     cleaninfo = sql.SltTeacherdata_orihtml(tid)[0][0]
    #     # doc_clean = dealHtml(doc_html)
    #     sql.UpdateTeacher_new_info(tid,cleaninfo)

#-----清洗html标签，结果存入teacher_new中------
    # teacherlist = sql.SltTeacher_new_id()
    # tidlist = [x[0] for x in teacherlist]
    # for tid in tidlist:
    #     doc_html = sql.SltTeacherdata_orihtml(tid)[0][0]
    #     doc_clean = dealHtml(doc_html)
    #     sql.UpdateTeacher_new_info(tid,doc_clean)





    pass

