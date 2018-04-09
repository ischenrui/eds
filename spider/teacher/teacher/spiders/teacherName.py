# -*- coding: utf-8 -*-
import scrapy
import codecs
import urllib
import time
import re
import json
from scrapy.http import HtmlResponse
from scrapy.http import XmlResponse
from scrapy.http import Request
from teacher.util.xin import *
from teacher.util.mysql import *

class CnkiListSpider(scrapy.Spider):
    name = 'teacherName'
    xin=Xin()
    nameList = []
    start_urls = ['http://epe.xjtu.edu.cn']
    mysql=Mysql()
    body=''
    nodePath=[]
    len=4
    domain=''
    url=''
    school=''
    p={}

    def parse(self, response):
        # self.school=self.mysql.getSchool()
        # url=self.school[3]
        url='http://www.math.pku.edu.cn/static/quanzhijiaoyuan.html'
        self.url=url
        print(url)
        self.domain =self.getDomain(url)
        yield scrapy.Request(url,dont_filter=True, callback=self.parseLink)

    def parseLink(self, response):
        self.body=self.getBody(response)
        dr = re.compile(r'<[^>]+>', re.S)
        bodyStr=''
        for b in self.body:
            bodyStr+=' ' +b.extract()
        info = dr.sub(' ',bodyStr)
        # info = self.body.xpath('string(.)').extract()[0]
        # print(bodyStr)
        info=self.replaceWhite(info)
        infoList=info.split(' ')
        for inf in infoList:
            isName=self.xin.isXin(inf)
            if isName==1:
                self.nameList.append(inf)
                node=self.getNode(inf)
                if len(node)==0:
                    continue
                node=node[0]
                path=self.getPathNode(node)
                self.nodePath.append(path)

        maxPath = self.getMatchPath()

        for  t in self.p:
            if len(maxPath)==0:
                break
            teacherList=self.getTeacherList(maxPath)
            value=self.getNameValue(teacherList)
            print('value:'+str(value))
            if value<0.3:
                print("错误")
            elif value>0.5:
                print("正确")
            else :
                print("存疑")
                self.printTeacher(teacherList)
                print("筛选")
                teacherList=self.selectByUrl(teacherList)
            maxPath = self.deleteAndGetMax(maxPath)
            if value>=0.3:
                pass
                # self.printTeacher(teacherList)
        # self.mysql.updateSchool(self.school[0])
        # self.school=self.mysql.getSchool()
        # url=self.school[3]
        # self.url=url
        # print(url)
        # self.domain =self.getDomain(url)
        # yield scrapy.Request(url, callback=self.parseLink)

    def selectByUrl(self,teacherList):
        cla={}
        teacher={}
        for key in teacherList:
            l=len(key)
            if str(l) in cla.keys():
                cla[str(l)]['all']+=1
            else:
                item={}
                item['is']=0
                item['all'] = 1
                cla[str(l)] =item
            isName = self.xin.isXin(teacherList[key])
            if isName == 1:
                cla[str(l)]['is'] += 1
        for key in teacherList:
            l=len(key)
            item=cla[str(l)]
            if item['all']!=0 and item['is']/item['all']>=0.5:
                teacher[key]=teacherList[key]
        return teacher

    def printTeacher(self,teacherList):
        for key in teacherList:
            print('name:'+key+': link:'+teacherList[key])
            item={}
            item['school']=self.school[1]
            item['institution']=self.school[2]
            item['institution_url']=self.url
            item['name'] = teacherList[key]
            item['link']=key
            self.mysql.insertTeacherLink(item)

    def deleteAndGetMax(self,maxPath):
        self.p[maxPath] = -1
        maxKey = ''
        maxNum = 0
        for key in self.p:
            if maxNum < self.p[key]:
                maxNum = self.p[key]
                maxKey = key
        return maxKey

    def getTeacherList(self,maxPath):
        xpath=self.praseXpath(maxPath)
        aList=self.body.xpath('./'+xpath)
        teacher={}
        for a in aList:
            name=self.setValue(a.xpath('string(.)'),'a').strip()
            aNode=self.findA(a)

            if aNode is None:
                continue
            link = self.setValue(aNode.xpath('./@href'),'href')
            if link in teacher.keys():
                isName = self.xin.isXin(name)
                if isName == 1:
                    teacher[link] = name
            else :
                teacher[link] = name
        return teacher

    def getNameValue(self,teacherList):
        sum=0
        num=0
        for t in teacherList:
            sum+=1
            isName = self.xin.isXin(teacherList[t])
            if isName == 1:
                num+=1
        if sum==0:
            return 0
        else :
            return num/sum

    def getTeacherUrl(self,url):
        url=url.strip()
        if len(url)==0:
            return ' '
        if url[0:4]=='http':
            return url
        if url[0]=='/':
            return self.domain+url
        else :
            index=self.url.rfind('/')
            return self.url[0:index+1]+url

    def praseXpath(self,path):
        xpath=''
        temp=path.split('&')
        ele=temp[0].split(' ')
        cla=temp[1].split(',')
        for  index,val in enumerate(ele):
            if len(val)==0:
                continue
            xpath+="/"+val
            c=cla[index]
            if (len(c)!=0) and (c!=' '):
                xpath+="[@class='"+c+"']"
        return xpath

    def findA(self,node):
        item=self.getElementId(node)
        if item is None:
            return None
        if item[0]=='a' or item[0]=='A':
            href=node.xpath('./@href').extract()
            if len(href)!=0 and href[0]!='#':
                return node
        aEle=self.findNextA(node)
        if len(aEle)==0:
            parent=self.getParent(node)
            return self.findA(parent)
        else:
            return aEle[0]

    def findNextA(self,node):
        aEle=node.xpath("./a[@href!='#' and not(contains(@href,'.edu.cn'))]")
        if len(aEle) == 0:
            aEle = node.xpath("./*/a[not (contains(@href,'.edu.cn')) and @href!='#']")
            if len(aEle) == 0:
                aEle = node.xpath("./*/*/a[not (contains(@href,'.edu.cn')) and @href!='#']")
                return aEle
            else:
                return aEle
        else :
            return aEle

    def getMatchPath(self):
        path=self.getMaxPath()
        if len(path)==0:
            return ''
        temp=path.split('&')[1]
        if self.len*2>=len(temp) and self.len<=6:
            self.len+=1
            self.getOnePathNode()
            return self.getMatchPath()
        else :
            return path

    def getMaxPath(self):
        self.p={}
        for t in self.nodePath:
            key=t['path']+'&'+t['class']
            if key in self.p:
                self.p[key]+=1
            else :
                self.p[key] =1
        maxKey=''
        maxNum=0
        for key in self.p:
            if maxNum<self.p[key]:
                maxNum=self.p[key]
                maxKey=key
        return maxKey

    def getOnePathNode(self):
        for path in self.nodePath:
            if not path['parent'] is None:
                element = self.getElementId(path['parent'] )
                if not element is None:
                    path['path'] = element[0] + " " + path['path']
                    path['class'] = element[2] + "," + path['class']
                    path['id'] = element[1] + " " + path['id']
                    temp = self.getParent(path['parent'])
                    path['parent'] = temp

    def getPathNode(self,node):
        path={}
        temp=node
        path['node']=temp
        path['parent']=temp
        path['path'] = ''
        path['id']=''
        path['class']=''
        for i in range(1,self.len+1):
            element = self.getElementId(temp)
            if not element is None:
                path['path'] =element[0]+" "+path['path']
                path['class'] = element[2] + "," + path['class']
                path['id'] = element[1]+" "+path['id']
                temp = self.getParent(temp)
                path['parent'] = temp
        return path

    def getElementId(self,node):
        if node is None:
            return None
        cla=self.setValue(node.xpath('./@class'),' ')
        elementStr=str(node.root)
        item=[]
        element=elementStr.split(' ')
        item.append(element[1])
        try:
            temp=element[3]
        except:
            return None
        item.append(temp[0:-1])
        item.append(cla)
        return item

    def getParent(self,node):
        parent = node.xpath("./parent::*")
        if len(parent)==0:
            return None
        else:
            return parent[0]

    def getNode(self,name):
        str = "//*[text()='" + name + "']"
        node = self.body.xpath(str)
        if len(node)==0:
            str = "//*[contains(text(),'" + name + "')]"
            node = self.body.xpath(str)
            return node
        else :
            return node

    def replaceWhite(self,info):
        p1 = re.compile('\s+')
        # p2=re.compile('[a - zA - Z0 - 9]+')
        # info = re.sub(p2, " ",info)
        new_string = re.sub(p1, ' ', info)
        return new_string

    def setValue(self, node, value):
        if len(node):
            return node.extract()[0]
        else:
            return value

    def getBody(self,response):
        body = response.xpath("//html")
        if len(body)>=2:
            return body
        body=response.xpath("//body")
        if len(body)==0:
            if type(response) == XmlResponse:
                body = response.xpath("//Page")
                return body
            else :
                return response.xpath('//*')
        else :
            return body
    def getDomain(self,url):
        reg = r'^https?:\/\/([a-z0-9\-\.]+)[\/\?]?'
        m = re.match(reg, url)
        uri = m.groups()[0] if m else ''
        temp=uri[uri.rfind('.', 0, uri.rfind('.')) + 1:]
        index=url.index(temp)+len(temp)
        return url[0:index]

    def getKeyValue(self, url, key):
        try:
            index = url.index('?')
            query = url[index + 1:]
            paramList = query.split('&')
            for p in paramList:
                temp = p.split('=')
                if temp[0].lower() == key:
                    return temp[1]
        except:
            print(url)
