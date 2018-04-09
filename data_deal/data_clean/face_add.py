from aip import AipFace
import os,shutil
import pymysql
import base64
from PIL import Image,ImageDraw
import time
import requests
from json import JSONDecoder

class Mysql(object):
    connect = pymysql.Connect(
        host='120.78.201.159',
        port=3306,
        user='root',
        passwd='zdf.0126',
        db='eds',
        charset='utf8'
)
# 获取游标
    cursor = connect.cursor()

# 插入图片info
    def InsertP(self, id,picinfo):
        sql = "INSERT INTO picinfo VALUES(%s,%s)"
        params = (id,picinfo)
        self.cursor.execute(sql, params)
        self.connect.commit()

    def InsertPic(self, id,ss):
        sql = "update teacher_add set pic=%s where id=%s "
        params = (ss,id)
        self.cursor.execute(sql, params)
        self.connect.commit()

    def SltTid(self):
        sql = "SELECT id FROM picinfo "
        self.cursor.execute(sql)
        return self.cursor.fetchall()

""" 你的 APPID AK SK """
APP_ID = '10909275'
API_KEY = 'q1jLbdVpVbLmM7cIGiw2O0kt'
SECRET_KEY = 'yzB9cHPyCHPGTPztUFTqYonGw6vThssR'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

def mymovefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print("move %s -> %s"%( srcfile,dstfile))

def faceDetect(path,toPath):

    http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
    data = {
        "api_key": "mCfBN23JWgwYFHyhlEWoB7mpIVh8HuW5",
        "api_secret": "x44kBrjgCVddv6MynjXryXjT9hjjkxYN"
    }

    f = open(path, "rb")
    files = {"image_file": f}
    response = requests.post(http_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    response.close()
    req_dict = JSONDecoder().decode(req_con)
    f.close()
    if "error_message" in req_dict.keys():
        print("发生了错误：")
        print(req_dict)
        return


    print(req_dict)
    # img = Image.open(path)
    # img_d = ImageDraw.Draw(img)
    # face = req_dict["faces"]
    # for f in face:
    #     face_rectangle = f["face_rectangle"]
    #     img_d.rectangle((face_rectangle['left'], face_rectangle['top'],
    #                      face_rectangle['left'] + face_rectangle['width'],
    #                      face_rectangle['top'] + face_rectangle['height']), outline="red")
    # img.save(toPath)
    # img.close()
    # time.sleep(5)


def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root) #当前目录路径
        # print(dirs) #当前路径下所有子目录
        # print(files) #当前路径下所有非目录子文件
        return files

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def getPicinfo(imagename):
    image = get_file_content(imagename)
    # """ 调用人脸检测 """
    # a = client.detect(image);

    """ 如果有可选参数 """
    options = {}
    options["max_face_num"] = 10
    # options["face_fields"] = "age"

    """ 带参数调用人脸检测 """
    a = client.detect(image, options)
    if a['result']==1:
        b = a['result'][0]['location']
        b ['result_num'] = a['result_num']
    else:
        b = a
    return b

if __name__ == '__main__':
    sql  = Mysql()

    # file_dir = 'testjpg'
    # imglist = file_name(file_dir)
    # for img in imglist:
    #     id = img.split('.')[0]
    #     sql.InsertPic(id,'ProfileImgs/'+id+'.jpg')

    # # ----将really内的图片改名，并将图片识别信息存入数据库----
    # imglist = file_name('temp/only/really')
    # fo = open('picinfo.txt')
    # for line in fo:
    #     if len(line)>0:
    #         picinfo = eval(line)
    #         # print(picinfo)
    #         imgname = picinfo['imgname']
    #         print(picinfo['picid'])
    #         # if imgname in imglist:
    #         sql.InsertP(picinfo['picid'],line)
                # os.rename('temp/only/really/'+imgname,'temp/only/really/'+str(picinfo['picid'])+'.jpg')



    # #----Y中唯一的id的图片剪切至really-----
    # picdic = {}
    # imglist = file_name('temp/only/Y')
    # for node in imglist:
    #     pid = node.split('-')[0]
    #     # print(pid)
    #     if pid in picdic.keys():
    #         picdic[pid][0] += 1
    #     else:
    #         list = [1,node]
    #         picdic[pid] = list
    # # print(picdic)
    #
    # for k, v in picdic.items():
    #     if v[0] == 1:
    #         mymovefile('temp/only/Y/%s'%(v[1]),'temp/only/really/%s'%(v[1]))


    # #---分类 Y是人脸 N不是人脸----
    # file_dir = 'temp/only'
    #
    # fo = open('temp/only/picinfo.txt')
    # for line in fo:
    #     picinfo = eval(line)
    #     imgname = picinfo['imgname']
    #     if picinfo['result_num'] == 1:
    #         mycopyfile('temp/only/imgs/'+imgname,'temp/only/Y/'+imgname)
    #     # else:mycopyfile('temp/only/img/'+imgname,'temp/only/N/'+imgname)

    #----图片识别下载------
    # file_dir = 'img'
    # imglist = file_name(file_dir)
    # for imgname in imglist:
    #     try:
    #         picid = imgname.split('-')[0]
    #         resultdir = getPicinfo(file_dir+ '/'+imgname)
    #         resultdir['picid'] = picid
    #         resultdir['imgname'] = imgname
    #         print(resultdir)
    #         # print(resultdir)
    #         fo = open("picinfo.txt", "a")
    #         fo.write(str(resultdir))
    #         fo.write('\n')
    #         time.sleep(1)
    #         fo.close()
    #     except:
    #         print(imgname+'错误')

#-----------------------------------------------------






    # resultdir = getPicinfo('testjpg/22-2.jpg')
    # resultdir['picid'] = 1
    # resultdir['imgname'] = 2
    # print(resultdir)

    # fo = open("temp/only/picinfo.txt")
    # fo.write(str(resultdir))

    # a = fo.readline()
    #
    # b = eval(a)
    # print(b['result_num'])



    pass



