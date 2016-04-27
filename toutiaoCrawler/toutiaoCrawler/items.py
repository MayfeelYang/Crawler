# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ToutiaocrawlerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tag = Field()
    title = Field()
    url = Field()
    datetime = Field()
    content = Field()
    comments = Field()
    id = Field()
    pass
