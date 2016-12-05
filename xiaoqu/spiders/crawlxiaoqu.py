#-*- encoding:utf-8 -*-

import scrapy
from scrapy import Selector
from xiaoqu.items import XiaoquItem

class crawlxiaoqu(scrapy.Spider):

    name = 'xiaoqu'
    start_urls = ['http://gz.lianjia.com/xiaoqu/pg%d' % d for d in range(1,100,1)]
    #start_urls = ['http://gz.lianjia.com/xiaoqu']

    def parse(self, response):
        sel = Selector(response)
        #小区名
        xiaoqu = sel.xpath('//div[@class="title"]/a/text()').extract()
        #小区均价
        meanPrice = sel.xpath('//div[@class = "totalPrice"]/span/text()').extract()
        #小区位置
        p1 = sel.xpath('//a[@class = "district"]/text()').extract()
        p2 = sel.xpath('//a[@class = "bizcircle"]/text()').extract()
        #position = p1+p2
        #小区建成时间
        buildTime = sel.xpath('//div[@class = "positionInfo"]/text()[4]').extract()
        #小区当前在售数量
        onSellCount = sel.xpath('//div[@class="xiaoquListItemSellCount"]/a/span/text()').extract()
        #90天内成交额
        sellOut= sel.xpath('//div[@class="houseInfo"]/a/text()').extract()

        item = XiaoquItem()
        for i in range(29):
            item['xiaoqu'] = xiaoqu[i].strip()
            item['position'] = p1[i].strip()+p2[i].strip()
            item['buildTime'] = buildTime[i].strip().replace(' ','').replace('\t','')
            item['onSellCount'] = onSellCount[i].strip()
            item['sellOut'] = sellOut[i].strip()
            item['meanPrice'] = meanPrice[i].strip()
            yield item
