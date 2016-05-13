#-*-coding:utf-8-*-
from scrapy.spider import Spider
from scrapy.selector import Selector
#from allpapers.items import PaperItem
from scrapy import Request
from scrapy import log
from datetime import datetime
import re
import requests
from zhihuCrawler.items import questionItem



class ZhihuSpider(Spider):

    name = "question"
    download_delay = 1
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/topic/19552832/questions']

    def parse(self,response):
        #response_selector = Selector(response)
        #question_list = response_selector.xpath('//*[@id="zh-topic-questions-list"]/div[1]/link/@href').extract()
        
        first_url = 'https://www.zhihu.com/topic/19552832/questions?page={page_index}'
        for index in range(1,10):
            next_url = first_url.replace('{page_index}',str(index))
            yield Request(url=next_url, callback=self.parse_page)


    def parse_page(self, response):
        sel = Selector(response)
        question_url = sel.xpath('//*[@id="zh-topic-questions-list"]/div[1]/link/@href').extract()
        for list in question_url:
            question_list = 'https://www.zhihu.com' + list
            yield Request(url=question_list, callback=self.parse_content)

    def parse_content(self,response):
        item = questionItem()
        sel = Selector(response)
        item['url'] = str(response.url)
        item['title']= sel.xpath('//*[@id="zh-question-title"]/h2').extract()
        item['content']=sel.xpath('//*[@id="zh-question-detail"]/div/text()').extract()

        return item