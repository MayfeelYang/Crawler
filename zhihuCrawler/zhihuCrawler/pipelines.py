# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZhihucrawlerPipeline(object):
    '''
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', host = '127.0.0.1', db = 'ZhihuCrawler',
                user = 'root', passwd = '14152069', cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8', use_unicode=True)
    '''

    def process_item(self, item, spider):
    	#query = self.dbpool.runInteraction(self._insert, item, spider)
        return item
    
    def _insert(self, conn, item, spider):
    	conn.execute("""
            insert into question (url, title, content)
            values(%s, %s, %s)
            """, (item['title'].encode('utf-8'),item['url'], item['content']))
    	conn.execute("""
            insert into recommend (url, title, content, answer)
            values(%s, %s, %s, %s)
            """, (recommend_Item['url'], recommend_Item['title'].encode("utf-8"), recommend_Item['content'].encode("utf-8"), recommend_Item['answer'].encode("utf-8")))
    #获取url的md5编码
    def _get_linkmd5id(self, item):
        #url进行md5处理，为避免重复采集设计
        return md5(item['link']).hexdigest()

    #异常处理
    def _handle_error(self, failue, item, spider):
        log.err(failure)
