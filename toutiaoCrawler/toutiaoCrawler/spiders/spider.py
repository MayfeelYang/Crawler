# -*- coding:utf8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from scrapy.http import Request
from toutiaoCrawler.items import ToutiaocrawlerItem
import re
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class ToutiaoSpider(RedisSpider):
    name = 'toutiaospider'
    redis_key = 'toutiaospider:start_urls'
    start_urls = ['http://toutiao.com/api/article/recent/?count=20000']

    def parse(self, response):
        item = ToutiaocrawlerItem()
        print  "****************"
        selector = Selector(response)
        news_list = json.loads(selector.xpath("//p/text()").extract()[0].encode("utf-8"))['data']
        print len(news_list)
        for news in news_list:
            item['tag'] = news['tag']
            item['title'] = news['title']
            item['url'] = news['display_url']

            item['datetime'] = news['datetime']
            yield Request(news['display_url'], callback = 'parseContent', meta = {'item': item})

    def parseContent(self, response):
        selector = Selector(response)
        item = response.meta['item']
        text_fields = None
        try:
            html = selector.xpath('//div[@class="article-content"]').extract()[0]
            text_fields = re.findall(r'<p.*?>(.*?)</p>', html, re.S)
        except Exception, e:
            print "$$$$$$$$$$$$$$possible gmw url", str(e)
            pass   
        full_text = ''
        if text_fields is not None: 
            for each in text_fields:
                full_text += each
            item['content'] = full_text
            return item