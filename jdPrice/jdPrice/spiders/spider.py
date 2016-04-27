# -*- coding:utf8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from scrapy.http import request
from jdPrice.items import JdpriceItem


import sys
reload(sys)
sys.setdefaultencoding('utf8')

class jdPriceSpider(RedisSpider):
    name = 'jdpricespider'
    redis_key = 'jdpricespider:start_urls'
    start_urls = ['http://channel.jd.com/1713-3287.html']

    def parse(self, reponse):
        item = JdpriceItem()
        selector = Selector(response)
        html_area = selector.xpath("//li[start-with(@clstag, 'channel|keycount')]")
        
