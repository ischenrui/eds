

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
class CnkiSpider(scrapy.Spider):
    name = 'teacherifream'
    start_urls = ['http://www.cnki.net']
    mysql=Mysql()
    list=[]
    def parse(self, response):
        self.school=self.mysql.getSchool()
        url=self.school[3]
        self.domain = self.getDomain(url)
        self.url=url
        print(url)
        yield scrapy.Request(url, callback=self.parseLink)

    def parseLink(self, response):
        src=response.xpath('//iframe/@src')
        for s in src:
            url=s.extract()
            link=self.getTeacherUrl(url)
            print("link---------------------------------")
            print(link)
            item = {}
            item['link'] = self.url
            item['iframe'] = link
            self.list.append(item)
        self.mysql.updateSchool(self.school[0])
        self.school = self.mysql.getSchool()
        try:
            url = self.school[3]
        except:
            for l in self.list:
                print('link:'+l['link'])
                print('ifram:' + l['iframe'])
        self.url = url
        print(url)
        self.domain = self.getDomain(url)
        yield scrapy.Request(url, callback=self.parseLink)
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
        else :
            index=self.url.rfind('/')
            return self.url[0:index+1]+url