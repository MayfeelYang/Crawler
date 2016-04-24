# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TombcrawlerPipeline(object):

    def __init__(self):
        #host = settings['MONGODB_HOST']
        #port = setttings['MONGODB_PORT']
        #dbName = settings['MONGODB_DBNAME']
        #client = pymongo.MongoClient(host = host, port = port)
        #tdb = client[dbName]
        #self.post = tdb[settings['MONGODB_DOCNAME']]
        pass

    def process_item(self, item, spider):
        bookInfo = dict(item)
        #self.post.insert(bookInfo)
        f = open('out', 'a')
        f.write(item['text'])
        f.write("\n")
        f.write("\n**************************")
        print item
        return item
