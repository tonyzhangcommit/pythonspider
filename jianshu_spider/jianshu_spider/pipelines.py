# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class JianshuSpiderPipeline:
    def __init__(self):
        dbparams = {
            'host':'127.0.0.1',
            'user':'root',
            'password':'mysqlroot',
            'port':3306,
            'database':'jianshu',
            'charset':'utf8',
        }
        self.conn = pymysql.connect(**dbparams)
        print(self.conn)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        print(item['title'],item['content'],item['author'],item['article_id'],item['origin_url'])
        print('*'*1000)
        self.cursor.execute(self.sql,(item['title'],item['content'],item['author'],item['article_id'],item['origin_url']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,author,article_id,origin_url) values(null,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql
from twisted.enterprise import adbapi
from pymysql import cursors

class JianshutwistedPipeline:
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'mysqlroot',
            'port': 3306,
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql',**dbparams)
        self._sql = None


    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into article(id,title,content,author,article_id,origin_url,avatar,pub_time,read_count,word_count,subjects) values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item,item)
        defer.addErrback(self.handle_error,item,spider)

    def insert_item(self,cursor,item):
        cursor.execute(self.sql,(item['title'],item['content'],item['author'],item['article_id'],item['origin_url'],item['avatar'],item['pub_time'],item['read_count'],item['word_count'],item['subjects']))

    def handle_error(self,error,item,spider):
        print('='*1000)
        print(error)
        print('='*1000)
