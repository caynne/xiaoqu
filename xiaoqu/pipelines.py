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
import time
#import MySQLdb
#import MySQLdb.cursors
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

filename = os.path.join('/Users/zidongceshi/code/xiaoqu/xiaoqu/analysis',time.strftime('%Y%m%d',time.localtime(time.time())))
filename = filename + '.csv'
'''
config = {
    'host':'localhost',
    'port':3306,
    'user':'root',
    'passwd':'1234',
    'db':'house',
    'charset':"utf8", #不加这个,在mysql中会以乱码显示中文
    'cursorclass':MySQLdb.cursors.DictCursor,
}


def connDB():
    db = MySQLdb.connect(**config)
    return db
'''

class XiaoQuWriteToCsv(object):
    def write_to_csv(self,item):
        csvwriter = csv.writer(codecs.open(filename,'a',encoding='utf-8'))
        csvwriter.writerow([item[key] for key in item.keys()])

    def process_item(self,item,spider):
        self.write_to_csv(item)
        return item

'''
class BargainWriteToDB(object):
    def process_item(self,item,spider):
        conn = connDB()
        cursor = conn.cursor()
        value = [item['area'],item['title'],item['houseName'],item['houseType'],item['houseSize'],item['dealPrice'],item['dealDate'],item['unitPrice'],item['direction'],item['elevator'],item['decoration'],item['floor'],item['buildDate'],item['originalPrice']]
        try:
            cursor.execute('INSERT INTO bargain (area,title,houseName,houseType,houseSize,dealPrice,dealDate,unitPrice,direction,elevator,decoration,floor,bulidDate,originalPrice) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
            conn.commit()
        except Exception,e:
            print e
            conn.rollback()
        return item
'''