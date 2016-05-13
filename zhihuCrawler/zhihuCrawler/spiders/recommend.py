# -*- coding:utf8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from zhihuCrawler.items import questionItem
from zhihuCrawler.items import recommendItem
import re
import json
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class ToutiaoSpider(RedisSpider):
    name = 'recommendspider'
    login_url = 'https://www.zhihu.com/login/email'
    start_urls = ['https://www.zhihu.com']
    url_header = 'https://www.zhihu.com'
    param1 = 'params={"offset":'
    param2 = ',"type":"day"}'
    
    def parse(self, response):
        # 获取_xsrf值
        _xsrf = response.css('input[name="_xsrf"]::attr(value)').extract()[0]
        # 获取验证码地址
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + str(time.time() * 1000)
        # 准备下载验证码
        yield Request(
            url = captcha_url,
            meta = {
                'cookiejar': 1,
                '_xsrf': _xsrf
            },
            callback = self.download_captcha
        )

    def download_captcha(self, response):
        # 下载验证码
        with open('captcha.gif', 'wb') as fp:
            fp.write(response.body)
        # 输入验证码
        print 'Please enter captcha: '
        captcha = raw_input()

        yield FormRequest(
            url = self.login_url,
            formdata = {
                'email': '1544344731@qq.com',
                'password': 'SpiderTestSuccess',
                '_xsrf': response.meta['_xsrf'],
                'remember_me': 'true',
                'captcha': captcha
            },
            meta = {
                'cookiejar': response.meta['cookiejar']
            },
            callback = 'parse_start'
        )

    def parse_start(self, response):
        first_url = 'http://www.zhihu.com/node/ExploreAnswerListV2?'
        for i in range(1,19):
            recommend_url = first_url + self.param1 + str(i * 5) + self.param2
            #print "URL:$$$$$$$$$$$", recommend_url
            yield Request(url=recommend_url, callback = 'parse_page', meta = {'cookiejar' : response.meta['cookiejar']})


    def parse_page(self, response):
        selector = Selector(response)
        url_list = selector.xpath('//div[@class= "explore-feed feed-item"]/h2/a')
        #question_title = selector.xpath("/html/body/div[1]/h2/a/text()")
        for each in url_list:
            url = each.xpath('@href').extract()[0].split('answer')[0]
            question_title = each.xpath('text()').extract()[0]
            complete_url = self.url_header + url
            question_id = url.split('/')[2]
            params = '{"url_token":' + str(question_id) + ',"pagesize":150,"offset":0}'
            frmdata = {"method": "next", "params": params, "_xsrf": '3d32031be5d0674566439af010e8ab83'}
            answer_url = "https://www.zhihu.com/node/QuestionAnswerListV2"
            yield FormRequest(answer_url, formdata = frmdata, callback = 'parseAnswer', meta = {'question_id' : question_id, 'question_title' : question_title, 'complete_url' : complete_url})
            
    def parseAnswer(self, response):
        question_id = response.meta['question_id']
        question_title = response.meta['question_title']
        complete_url = response.meta['complete_url']
        #print "**************" , json.loads(response.body_as_unicode())['msg'][1].decode('utf-8')
        res = json.loads(response.body_as_unicode())['msg']
        answer_list = []
        f_author = open("author_error" , 'a')
        for each in res:
            tmp_dict = {}
            selector = Selector(text = each)
            answer_content = selector.xpath('//div[@class="zm-editable-content clearfix"]/text()|//div[@class="zm-editable-content clearfix"]/b/text()|//div[@class="zm-editable-content clearfix"]/ul/li/text()').extract()
            #print (''.join(answer_content)).decode('utf-8')
            tmp_dict['answer_content'] = ''.join(answer_content)
            try:
                tmp_dict['answer_author'] = (selector.xpath('//a[@class="author-link"]/text()|//div[@class = "zm-item-answer-author-info"]/span[@class = "name"]/text()').extract())[0]
            except Exception,e:
                f_author.write("************" + str(complete_url) + "\n")
            tmp_dict['answer_time'] = (selector.xpath('//a[@class="answer-date-link meta-item"]/text()').extract())[0]
            tmp_dict['answer_support'] = (selector.xpath('//span[@class="count"]/text()').extract())[0]
            # answer_author = selector.xpath .......

            #dict completed
            answer_list.append(tmp_dict)

        #the elements of the answer_list is a dict
        # each dict has some key , e.g. 'anwser_author','anwser_content','answer_time', 'answer_support'
        yield Request(complete_url, callback = 'parseQuestion', meta = {'question_id' : question_id, 'question_title' : question_title, 'complete_url' : complete_url, 'answer_list' : answer_list})

    def parseQuestion(self, response):
        #print "********\n", self.getAnswer()
        selector = Selector(response)
        recommend_Item = recommendItem()
        recommend_Item['question_id'] = response.meta['question_id']
        recommend_Item['question_title'] = response.meta['question_title']
        recommend_Item['url'] = response.meta['complete_url']
        tags_list = selector.xpath('//div[@class="zm-tag-editor-labels zg-clear"]/a/text()').extract()
        new_tags = []
        for tags in tags_list:
            new_tags.append(tags.strip())
        recommend_Item['tags'] = ','.join(new_tags)
        question_content_list = selector.xpath('//*[@id= "zh-question-detail"]/div/text()').extract()
        if len(question_content_list) != 0:
            recommend_Item['question_content'] = question_content_list[0]
        else:
            recommend_Item['question_content'] = 'NONE'
        recommend_Item['answer_num'] = (selector.xpath('//*[@id="zh-question-answer-num"]/text()').extract())[0].split()[0]
        recommend_Item['attention_num'] = (selector.xpath('//*[@id="zh-question-side-header-wrap"]/text()').extract()[1]).split()[0]
        recommend_Item['answer_list'] = response.meta['answer_list']
        return recommend_Item

