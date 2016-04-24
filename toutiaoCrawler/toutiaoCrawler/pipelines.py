# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class ToutiaocrawlerPipeline(object):
    #def process_item(self, item, spider):
        #return item
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

class ToutiaocrawlerPipeline2(object):
    def process_item(self, item, spider):
        return item



class JsonWithEncodingCnblogsPipeline(object):
    def __init__(self):
        self.file = codecs.open('cnblogs.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()

class ToutiaocrawlerPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', host = '127.0.0.1', db = 'CrawlerDB',
                user = 'root', passwd = '1qaz2wsx', cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        print "@@@@@@@@@@@"
        query = self.dbpool.runInteraction(self._insert, item, spider)
        #query.addErrback(self._handle_error, item, spider)
        return item

    def _insert(self, conn, item, spider):
        #linkmd5id = self._get_linkmd5id(item)
        #print linkmd5id
        #now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        #conn.execute("""
        #       select 1 from cnblogsinfo where linkmd5id = %s
        #""", (linkmd5id, ))
        #ret = conn.fetchone()

        #if ret:
        #    conn.execute("""
        #       update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
        #   """, (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id))
            #print """
            #    update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
            #""", (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id)
        #else:
        #   conn.execute("""
        #        insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated) 
        #        values(%s, %s, %s, %s, %s, %s)
         #   """, (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now))
            #print """
            #    insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated)
            #    values(%s, %s, %s, %s, %s, %s)
            #""", (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now)
        conn.execute("""
            insert into TouTiao (title, tag, datetime, url, content)
            values(%s, %s, %s, %s, %s)
            """, (item['title'].encode('utf-8'), item['tag'], item['datetime'], item['url'], item['content'].encode("utf-8")))
        print type(item['title'].encode('utf-8')), "((((((((((((((((((((("
        #log.msg("Item stored in db", level=log.DEBUG)


    #获取url的md5编码
    def _get_linkmd5id(self, item):
        #url进行md5处理，为避免重复采集设计
        return md5(item['link']).hexdigest()

    #异常处理
    def _handle_error(self, failue, item, spider):
        log.err(failure)