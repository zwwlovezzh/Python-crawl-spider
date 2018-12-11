#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-12-01 21:32:39
# Project: qidian1202

from pyspider.libs.base_handler import *
import re

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.qidian.com/all?orderId=8&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.book-mid-info > h4 > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        next = response.doc('.lbf-pagination-next').attr.href
        self.crawl(next, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        ss = response.text
        demo = response.doc('.book-info > p:nth-child(4) > em:nth-child(1)').text()
        patten = re.compile(r'font-family: (.*?); src:',re.S)
        demo = patten.findall(demo)[0]
        jmzt = 'https://qidian.gtimg.com/qd_anti_spider/{}.ttf'.format(demo)
        
        
        pattern1 = re.compile(r'<span class="' + demo + '">(.*?)</span>',re.S)
        ret = pattern1.findall(ss)    
        return {
            
            "url": response.url,
            "title": response.doc('title').text(),
            "图片链接": response.doc('.book-img > a > img').attr.src,
            "书名": response.doc('.book-info > h1 > em').text(),
            "作者": response.doc('div.book-info > h1 > span > a').text(),
            "解密字体库链接": jmzt,
            "字数": ret[0],
            "点击数": ret[1],
            "推荐数": ret[3],
            "书籍简介": response.doc('.book-intro > p').text(),
            "作品状态": response.doc('div.book-info > .tag > .blue').text(),
            "作品分类": response.doc('.book-info > .tag > .red').text(),
        }
