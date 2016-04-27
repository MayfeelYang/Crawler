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
    start_urls = ['http://toutiao.com/api/article/recent/?count=10&offset=100']

    def parse(self, response):
        item = ToutiaocrawlerItem()
        selector = Selector(response)
        news_list = json.loads(selector.xpath("//p/text()").extract()[0].encode("utf-8"))['data']
        for news in news_list:
            item['tag'] = news['tag']
            item['title'] = news['title']
            item['url'] = news['display_url']
            item['id'] =  news['id']
            item['datetime'] = news['datetime']

            yield Request(news['display_url'], callback = 'parseContent', meta = {'item': item, 'dis_url': news['display_url']})

    def parseContent(self, response):
        selector = Selector(response)
        item = response.meta['item']
        dis_url = response.meta['dis_url']
        comment_url = dis_url+"comments/?count=10&page=1&offset=0&format=json"

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
            return Request(comment_url, callback = 'parseComment', meta = {'item': item})


    def parseComment(self, response):
        item_comment = []
        selector = Selector(response)
        item = response.meta['item']
        try:
            comment_list = json.loads(selector.xpath("//p/text()").extract()[0].encode("utf-8"))['data']['comments']
            print "??????????????/", len(comment_list)
        except Exception, e:
            print "$$$$$$$$$$$$$$comment error", str(e)
            pass
        
        for comment in comment_list:
            tmp_dic = dict()
            tmp_dic['user_id'] = comment['user_id']
            tmp_dic['user_name'] = comment['user_name']
            tmp_dic['create_time'] = comment['create_time']
            tmp_dic['text'] = comment['text']
            item_comment.append(tmp_dic)
        item['comments'] =  item_comment
        
        return item





        