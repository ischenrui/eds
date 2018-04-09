

import scrapy
import codecs
import urllib
import time
import re
import json
import traceback
from scrapy.http import HtmlResponse
from scrapy.http import XmlResponse
from scrapy.http import Request
from teacher.util.xin import *
from teacher.util.mysql import *
class CnkiSpider(scrapy.Spider):
    name = 'teacher'
    start_urls = ['http://www.12371.cn/special/xxzd/jh/']
    mysql=Mysql()
    list=[]
    institution=''
    map={}
    def parse(self, response):
        li=self.mysql.getTeacher()
        for l in li:
            self.teacher=l
            url=self.teacher[5]
            self.institution =url
            link=self.teacher[2]
            self.domain = self.getDomain(url)
            self.url=url
            tLink=self.getTeacherUrl(link)
            self.map[tLink]=self.teacher[0]
            print(tLink)
            yield scrapy.Request(tLink, callback=self.parseLink)

    def parseLink(self, response):
        t={}
        try:
            t['id']=self.map[response.url]
        except:
            return
        t["original_html"]=self.replaceWhite(response.text)

        info =self.getBody(response)[0].xpath('string(.)').extract()[0]
        info = self.replaceWhite(info)
        t['info']=info
        imgs=response.xpath('//img/@src')
        imgStr=''
        for img in imgs:
            l=img.extract().strip()
            le=len(l)
            if le==0 or le>2048:
                continue
            imgStr+="-link-"+img.extract()
        t['image']=imgStr
        try:
            self.mysql.TeacherupdateHtml(t)
            print(t['id'])
        except :


            print(t['image'])
            pass
            # self.mysql.TeacherupdateHtml(t)

    def getBody(self,response):
        body = response.xpath("//html")
        if len(body)>=2:
            return body
        body=response.xpath("//body")
        if len(body)==0:
            if type(response) == XmlResponse:
                body = response.xpath("//Page")
                if len(body)==0:
                    body = response.xpath("//resume")
                return body
            else :
                return response.xpath('//*')
        else :
            return body
    def replaceWhite(self, info):
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
    def getDomain(self,url):
        reg = r'^https?:\/\/([a-z0-9\-\.]+)[\/\?]?'
        m = re.match(reg, url)
        uri = m.groups()[0] if m else ''
        temp=uri[uri.rfind('.', 0, uri.rfind('.')) + 1:]
        index=url.index(temp)+len(temp)
        return url[0:index]
    def getTeacherUrl(self,url):
        url=url.strip()
        if len(url)==0:
            return ' '
        if url[0:4]=='http':
            return url
        if url[0]=='/':
            return self.domain+url
        elif self.url[-1] == '/' and url[0] == '.':
            return self.url+url
        elif self.url[-1]=='/' :
            index = self.url[0:-1].rfind('/')
            if index==-1:
                l=self.url + url
            else :
                l=self.domain+'/'+url
            return l
        else :
            index=self.url.rfind('/')
            return self.url[0:index+1]+url