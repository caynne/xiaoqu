#-*- encoding:utf-8 -*-

import scrapy
from scrapy import Selector
from xiaoqu.items import XiaoquItem
from xiaoqu.items import BargainItem

class crawlxiaoqu(scrapy.Spider):

    name = 'bargain'
    start_urls = ['http://gz.lianjia.com/chengjiao/huanan1/pg%d' % d for d in range(1,16,1)]
    #start_urls = ['http://gz.lianjia.com/chengjiao/huanan1/pg1']

    def parse(self, response):
        sel = Selector(response)
        #房名
        #houseName
        info = response.selector.xpath("//div[@class='info']/div[@class='title']/a/text()").extract()
        houseName = []  #小区名
        houseType = []  #户型
        houseSize = []  #大小
        for i in xrange(0,len(info)):
            temp = info[i].split()
            try:
                houseName.append(temp[0])
            except:
                houseName.append('')
            try:
                houseType.append(temp[1])
            except:
                houseType.append('')
            try:
                houseSize.append(temp[2].strip('平米'))
            except:
                houseSize.append('')
        #成交价
        dealPrice = response.selector.xpath("//div[@class='totalPrice']/span/text()").extract()
        #成交时间
        dealDate = response.selector.xpath("//div[@class='dealDate']/text()").extract()
        #均价
        unitPrice =  response.selector.xpath("//div[@class='unitPrice']/span/text()").extract()
        houseInfo = response.selector.xpath("//div[@class='houseInfo']/text()").extract()
        direction  = [] #朝向
        elevator = [] #电梯
        decoration = [] #装修
        for i in xrange(0,len(houseInfo)):
            temp = houseInfo[i].split('|')
            try:
                direction.append(temp[0])
            except:
                direction.append('')
            try:
                elevator.append(temp[2])
            except:
                elevator.append('')
            try:
                decoration.append(temp[1])
            except:
                decoration.append('')


        bulidInfo = response.selector.xpath("//div[@class='positionInfo']/text()").extract()
        floor = [] #楼层
        bulidDate = [] #建造年代
        for i in xrange(0,len(bulidInfo)):
            temp = bulidInfo[i].split()
            try:
                floor.append(temp[0])
            except:
                floor.append('')
            try:
                date = int(temp[1][0:4])
                if date and isinstance(date,int):
                    bulidDate.append(date)
                else:
                    bulidDate.append(0)
            except:
                bulidDate.append(0)


        original = response.selector.xpath("//span[@class='dealCycleTxt']/span/text()").extract()
        originalPrice = [] #挂牌价
        dealCycle = [] #成交周期
        for i in range(0,len(original)):
            try:
                if original[i].startswith('挂牌'):
                    price = original[i]
                    price = price.lstrip('挂牌').rstrip('万')
                    originalPrice.append(int(price))
            except:
                originalPrice.append('')
                dealCycle.append('')

        bargain = BargainItem()
        for i in range(len(info)):
            bargain['houseName'] = houseName[i]
            bargain['houseType'] = houseType[i]
            bargain['houseSize'] = houseSize[i]
            bargain['dealPrice'] = dealPrice[i]
            bargain['dealDate'] = dealDate[i]
            bargain['unitPrice'] = unitPrice[i]
            bargain['direction'] = direction[i]
            bargain['elevator'] = elevator[i]
            bargain['decoration'] = decoration[i]
            bargain['floor'] = floor[i]
            bargain['buildDate'] = bulidDate[i]
            bargain['originalPrice'] = originalPrice[i]
            yield bargain
