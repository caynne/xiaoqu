#-*- encoding:utf-8 -*-

import scrapy
from scrapy import Selector
from xiaoqu.items import XiaoquItem
from xiaoqu.items import BargainItem
import json

class crawlxiaoqu(scrapy.Spider):

    name = 'bargain'
    start_urls = ['http://gz.lianjia.com/chengjiao/huanan1']
    #start_urls = ['http://gz.lianjia.com/chengjiao/huanan1/pg%d' % d for d in range(1,16,1)]
    #start_urls = ['http://gz.lianjia.com/chengjiao/huanan1/pg1']
    global cookies
    cookies = {'lianjia_uuid':'0247fbb6-c2f0-46a9-82fd-eca66dd54407',
            'miyue_hide':'%20index%20%20index%20%20index%20%20index%20%20index%20',
            '_jzqx=1.1474370550.1477047517.2.jzqsr':'gz%2Elianjia%2Ecom|jzqct=/.jzqsr=gz%2Elianjia%2Ecom|jzqct=/chengjiao/',
            '_qzja':'1.1491508772.1473303079895.1487578044787.1487585438292.1487585462512.1487585486125.0.0.0.72.14',
            '_jzqa':'1.2845263418918121500.1473303080.1487578045.1487585438.14',
            'UM_distinctid':'15ad6466b1230b-0d34d0806c368f-6a11157a-1fa400-15ad6466b15209',
            'lianjia_token':'2.0078a267ff01959927690f4ece983d2511',
            'Hm_lvt_678d9c31c57be1c528ad7f62e5123d56':'1490264834',
            'select_city':'440100',
            'all-lj':'1e9f8fe64a0d8d4cd8642eafcff9cfff',
            '_smt_uid':'57d0d228.5047bf44',
            'CNZZDATA1255849599':'1498381017-1473297753-%7C1491027071',
            'CNZZDATA1254525948':'830432583-1473300258-%7C1491024920',
            'CNZZDATA1255633284':'457444627-1473301265-%7C1491026849',
            'CNZZDATA1255604082':'2037584611-1473298644-%7C1491027051',
            '_gat':'1',
            '_gat_global':'1',
            '_ga':'GA1.2.862139384.1473303080',
            '_gat_dianpu_agen':'1',
            'lianjia_ssid':'7556199e-f2cd-e42e-1727-bd51e53858e6',
        }

    def parse(self,response):
        sel = Selector(response)
        info = response.selector.xpath("//div[@data-role='ershoufang']/div/a/@href").extract()
        asd = response.selector.xpath("//div[@class='crumbs fl']/a/text(").extract()
        position = []
        for item in info:
            position.append('http://gz.lianjia.com' + item)
        for url in position:
            yield scrapy.Request(url,callback=self.parse_position,cookies=cookies,meta={'area':item})

    def parse_position(self,response):
        area = response.meta.get('area')
        sel = Selector(response)
        info = response.selector.xpath("//div[@data-role='ershoufang']/div[2]/a/@href").extract()
        position = []
        for item in info:
            position.append('http://gz.lianjia.com'+item)
        for item in position:
            yield scrapy.Request(item,callback=self.parse_totalPage,cookies=cookies,meta={'area':area})

    def parse_totalPage(self,response):
        area = response.meta.get('area')
        page = response.selector.xpath("//div[@class='page-box house-lst-page-box']/@page-data").extract()
        if page:
            totalPage = json.loads(page[0])['totalPage']
            urlList = [response._url+ 'pg%d' % d for d in range(1,totalPage+1,1)]

            for url in urlList:
                yield scrapy.Request(url,callback = self.parse_chenjiao,meta={'area':area})
        else:
            yield scrapy.Request(response._url,cookies = cookies,callback = self.parse_chenjiao,meta={'area':area})

    def parse_chenjiao(self, response):
        area = response.meta.get('area')
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
        title = response.selector.xpath("//title/text()").extract()
        bargain['title'] = title[0][0:5]
        bargain['area'] = area
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
