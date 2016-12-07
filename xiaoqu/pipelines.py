# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import codecs
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# class XiaoquPipeline(object):
#     def __init__(self):
#         self.filePath = os.path.abspath(os.curdir)+'/xiaoqu.json'
#         self.file = codecs.open(self.filePath,'wb',encoding='utf-8')
#
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item),ensure_ascii=False)+'\n'
#         self.file.write(line)
#         return item

filename = os.path.abspath(os.curdir)+'/sechandhouse.csv'
class XiaoQuWriteToCsv(object):
    def write_to_csv(self,item):
        csvwriter = csv.writer(codecs.open(filename,'a',encoding='utf-8'))
        csvwriter.writerow([item[key] for key in item.keys()])

    def process_item(self,item,spider):
        self.write_to_csv(item)
        return item