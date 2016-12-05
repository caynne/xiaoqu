# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import codecs
import csv

class XiaoquPipeline(object):
    def __init__(self):
        self.filePath = os.path.abspath(os.curdir)+'/xiaoqu.json'
        self.file = codecs.open(self.filePath,'wb',encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(line)
        return item

class XiaoQuWriteToCsv(object):
    def __index__(self):
        self.path = os.path.abspath(os.curdir)+'xiaoqu.json'
        self.file = codecs.open(self.path,'wb',encoding='utf-8')
    def process_item(self,item,spider):
        cw = csv.writer(self.file)
        cw.writerow(['xiaoqu','position','buildTime','onSellCount','sellOut','meanPrice'])
        cw.writerow(item)