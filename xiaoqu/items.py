# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoquItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #小区名
    xiaoqu = scrapy.Field()
    #小区均价价
    meanPrice = scrapy.Field()
    #小区位置
    position = scrapy.Field()
    #小区建成时间
    buildTime = scrapy.Field()
    #小区当前在售数量
    onSellCount = scrapy.Field()
    #90天内成交额
    sellOut = scrapy.Field()

class BargainItem(scrapy.Item):
    title = scrapy.Field()
    houseName = scrapy.Field()
    houseType = scrapy.Field()
    dealPrice = scrapy.Field()
    houseSize = scrapy.Field()
    dealDate = scrapy.Field()
    unitPrice = scrapy.Field()
    direction = scrapy.Field()
    elevator = scrapy.Field()
    buildDate = scrapy.Field()
    dealCycle = scrapy.Field()
    originalPrice = scrapy.Field()
    decoration = scrapy.Field()
    floor = scrapy.Field()
    area = scrapy.Field()
