# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import  Item, Field

class ZhihucrawlerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZhihuItem(Item):
    url = Field()
    name = Field()

class questionItem(Item):
    title = Field()
    url = Field()
    content = Field()

class recommendItem(Item):
    question_title = Field()
    question_id = Field()
    url = Field()
    tags = Field()
    attention_num = Field()
    question_content = Field()
    answer_num = Field()
    answer_list = Field()
