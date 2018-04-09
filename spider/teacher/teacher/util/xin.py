
import re

from teacher.data.readName import *

class Xin(object):
    xin=[]
    filt=['关工委','博士后','党务','祝福','经典','家园','项目','幸福','博士后','毕业','交流','国内','党委','风采','班团','培训','平台','汇总','高峰','计划','荣誉','奖励','高等','教育学','高职','科学','党代会','党政','党团','支部','工作','全文','关闭','通讯','高级','党建','尚无','有用','应用','计算','相关','公共','成果','师资','全职','教师','顾问','海外','通知','公告','管理','毕业生','国际','马上','高端','全部','论文','计算机','学院','常用','下载','党群','组织','成就','关于','法治','法制']
    rep=['(',')','（','）',':','：',' ',' ','.',',','/','*','、','讲师','副教授','教授','客座','讲座','博士生导师','硕士','导师','博士','姓名','双聘','主任']
    def __init__(self):
        file="teacher/data/name.txt"
        self.xin=readXin(file)
    def findXin(self,name):
        for x in self.xin:
            try:
                index=name.index(x)
                if index==0:    #姓要出现在第一个
                    return 1
            except:
                pass
        return 0
    def reName(self,name):
        if name is None:
            print("None")
            return 1
        p1 = re.compile('\s+')
        # p2=re.compile('[a - zA - Z0 - 9]+')
        # info = re.sub(p2, " ",info)
        name = re.sub(p1, ' ', name)
        for r in self.rep:
            name = name.replace(r, ' ')
        return name
    def isXin(self,name):
        if name is None:
            print("None")
            return 1
        p1 = re.compile('\s+')
        # p2=re.compile('[a - zA - Z0 - 9]+')
        # info = re.sub(p2, " ",info)
        name = re.sub(p1, ' ', name)
        for r in self.rep:
            name=name.replace(r,'')
        name=re.sub('[a-zA-Z]+', '', name)
        for n in self.filt: #判断名字是否在过滤表上
            index = name.find(n)
            if index>=0:
                return 0
        l=len(name)
        if(l<2):     # 判断名字是否符合长度
            return 0
        if(l>5):
            return 0
        return self.findXin(name)