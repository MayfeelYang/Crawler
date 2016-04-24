# -*- coding :utf8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from scrapy.http import Request
from tombCrawler.items import TombcrawlerItem
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class TombSpider(RedisSpider):
    name = "tombspider"
    redis_key = 'tombspider:start_urls'
    start_urls = ['http://www.daomubiji.com/']
    def parse(self, response):
        selector = Selector(response)
        table = selector.xpath('//table')
        for each in table:
            bookName = each.xpath('tr/td[@colspan="3"]/center/h2/text()').extract()[0]
            content = each.xpath('tr/td/a/text()').extract()
            url = each.xpath('tr/td/a/@href').extract()
            #for i in range(len(url)):
            for i in range(1):
                item = TombcrawlerItem()
                item['bookName'] = bookName
                item['chapterURL'] = url[i]
                try:
                    item['bookTitle'] = content[i].split(' ')[0]
                    item['chapterNum'] = content[i].split(' ')[1]
                except Exception, e:
                    print "spider_error", str(e)
                    continue

                try:
                    item['chapterName'] = content[i].split(' ')[2]
                except Exception, e:
                    print "spider_", str(e)
                    item['chapterName'] = content[i].split(' ')[1][-3:]
                #yield item
                print item
                yield Request(url[i], callback = 'parseContent', meta = {'item': item})

    def parseContent(self, response):
        print "^^^^^^^^^^^^^^^^^"
        selector = Selector(response)
        item = response.meta['item']
        html = selector.xpath('//div[@class="content"]').extract()[0]
        textField = re.search(r'<div style="clear:both"></div>(.*?)<div', html, re.S).group(1)
        text = re.findall(r'<p>(.*?)</p>', textField, re.S)
        fulltext = ''
        for each in text:
            fulltext += each
        item['text'] = fulltext
        print "********************"
        print item
        yield item

