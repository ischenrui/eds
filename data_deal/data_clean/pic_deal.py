import os,shutil
from PIL import Image,ImageDraw
import numpy as np
import hashlib
import pymysql

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

    def SltTid(self,id):
        sql = "SELECT picinfo FROM picinfo where id=%s"
        params = (id)
        self.cursor.execute(sql,params)
        return self.cursor.fetchone()

def md5sum(filename):
    file_object = open(filename, 'rb')
    file_content = file_object.read()
    file_object.close()
    file_md5 = hashlib.md5(file_content).hexdigest()
    return file_md5

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root) #当前目录路径
        # print(dirs) #当前路径下所有子目录
        # print(files) #当前路径下所有非目录子文件
        return files

def mymovefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print("move %s -> %s"%( srcfile,dstfile))

def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))

def reface(img,location):
    x_len, y_len = img.size
    x = location['left']+location['width']/2
    y = location['top'] + location['height']/2


    if location['width']/0.5>200:
        x1 = x-location['width']
        y1 = y-location['height']*1.2
        y2 = y + location['height'] * 1.2
        x2 = x + (y2 - y1)*1.3

    else:
        x1 = x - 130
        y1 = y - 100
        x2 = x + 130
        y2 = y + 100
    if x1 < 0: x1 = 0
    if y1 < 0: y1 = 0
    if x2 > x_len: x2 = x_len
    if y2 > y_len: y2 = y_len
    box = (x1,y1,x2,y2)
    cropImg = img.crop(box)
    return cropImg

def cutpic(img,location):
    x_len, y_len = img.size
    x = location['left'] + location['width'] / 2
    y = location['top']

    if x_len == y_len: return img
    if x_len > y_len:
        D = x_len - y_len
        x1 = D * x/x_len
        x2 = x_len - D * (1-x/x_len)
        box = (x1, 0, x2, y_len)
        cropImg = img.crop(box)
        return cropImg
    if y_len > x_len:
        D = y_len - x_len
        y1 = D * y/y_len
        y2 = y_len - D * (1-y/y_len)
        box = (0, y1, x_len, y2)
        cropImg = img.crop(box)
        return cropImg



if __name__ == '__main__':
    sql = Mysql()


#----重命名----
    # onlylist = file_name('temp/only/Y')
    # for name in onlylist:
    #     print(name)
    #     newname = name.replace('imgs','')
    #     print(newname)
    #     os.rename('temp/only/Y/'+name,'temp/only/Y/'+newname)

#---移动2chongfu到only---
    # onlylist = file_name('temp/only/imgs')
    # pidonlylist = []
    # for onlyname in onlylist:
    #     pidonlylist.append(onlyname.split('-')[0])
    #
    # chongfulist = file_name('temp/2chongfu/imgs')
    # for chongfuname in chongfulist:
    #     chongfuid = chongfuname.split('-')[0]
    #     if chongfuid not in pidonlylist:
    #         mymovefile('temp/2chongfu/imgs/'+chongfuname,'temp/only/imgs/'+chongfuname)
    #         print(chongfuid)
    #         pidonlylist.append(chongfuid)


#---切割图片----
    file_dir = 'img'
    imglist = file_name(file_dir)
    for imagename in imglist:
        try:
            #------头像画框-----
            # imagename = '2.jpg'
            img = Image.open('img/'+imagename).convert('RGB')

            picid = imagename.split('.')[0]
            print(picid)
            img_d = ImageDraw.Draw(img)


            a = sql.SltTid(picid)[0]
            a = eval(a)
            b = a['result'][0]['location']

            #计算一些图片参数，包括长宽比，像素大小，脸占比
            x_len, y_len = img.size
            w = b['width']
            h = b['height']

            ckb = x_len/y_len   #长宽比
            xsdx = x_len*y_len  #像素大小
            lzb = w*h/xsdx  #脸占比
            #---获取 图片的 x轴，y轴 像素---
            # newpic = reface(img,b)
            newpic = cutpic(img,b)
            # #---剪切规则----
            # if ckb>0.9 and ckb<1.33:
            #     if xsdx>40000 and lzb<0.017:
            #         newpic = reface(img, b)
            #     else:newpic=img
            # else:
            #     if xsdx>40000:
            #         newpic = reface(img, b)
            newpic.save('testjpg/' + imagename)
        except:
            pass
        # newpic.close()
        # img.close()
        # img_d.line(((b['left'],b['top']),(b['left']+b['width'],b['top'])),(255, 0, 0))
        # img_d.line(((b['left'],b['top']),(b['left'],b['top']+b['height'])),(255, 0, 0))
        # img_d.line(((b['left']+b['width'],b['top']),(b['left']+b['width'],b['top']+b['height'])),(255, 0, 0))
        # img_d.line(((b['left'],b['top']+b['height']),(b['left']+b['width'],b['top']+b['height'])),(255, 0, 0))

        #----保存图片----

        # img.save('testjpg/result/r'+imagename)



#----分类图片-----
    # dir = {}
    # for node in imglist:
    #     name = file_dir+"/"+node
    #     md5 = md5sum(name)
    #     print(md5)
    #
    #     if md5 in dir.keys():
    #         dir[md5].append(name)
    #     else:
    #         list = [name]
    #         dir[md5] = list
    #
    # for v in dir.values():
    #     if len(v)>2:
    #         for imgname in v:
    #             mycopyfile(imgname,'temp/move/'+imgname)
    #     if len(v)==2:
            # if v[0].split('-')[0] == v[1].split('-')[1]:
            #     mymovefile(v[0], 'move/' + v[0])
            # else:
            #     for imgname in v:
            #         mymovefile(imgname, 'move/' + imgname)
        #     for imgname in v:
        #         mycopyfile(imgname,'temp/2chongfu/'+imgname)
        # if len(v)==1:
        #     mycopyfile(v[0], 'temp/only/' + v[0])
    pass









