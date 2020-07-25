# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter

import pymysql

# 报存数据到mysql
class FangPipeline:
    def __init__(self):
        dbparams = {
            'host':'127.0.0.1',
            'user':'root',
            'password':'mysqlroot',
            'port':3306,
            'database':'fangtianxia',
            'charset':'utf8',
        }
        self.conn = pymysql.connect(**dbparams)
        print(self.conn)
        self.cursor = self.conn.cursor()
        self._sqlnew = None
        self._sqlesf = None

    def process_item(self, item, spider):
        # print(item['title'],item['content'],item['author'],item['article_id'],item['origin_url'])
        # print('*'*1000)
        # self.cursor.execute(self.sql,(item['title'],item['content'],item['author'],item['article_id'],item['origin_url']))
        # self.conn.commit()
        if len(item) < 12:
            print("新房")
            self.cursor.execute(self.sqlnew, (item['province'], item['city'], item['name'],item['price'], ''.join(item['rooms']), item['area'], item['address'], item['district'], item['sale'], item['origin_url']))
            self.conn.commit()
        else:
            self.cursor.execute(self.sqlesf, (item['province'], item['city'], item['name'], item['rooms'], item['floor'], item['toward'], item['address'],item['year'], item['area'], item['price'],item['unit'],item['origin_url']))
            self.conn.commit()
        print(len(item))
        return item

    @property
    def sqlnew(self):
        if not self._sqlnew:
            self._sqlnew = """
            insert into newhouse(id,province,city,name,price,rooms,area,address,district,sale,origin_url)\
             values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sqlnew
        return self._sqlnew

    @property
    def sqlesf(self):
        if not self._sqlesf:
            self._sqlesf = """
            insert into esfhouse(id,province,city,name,rooms,floor,toward,address,year,area,\
            price,unit,origin_url) values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sqlesf
        return self._sqlesf


# 保存数据到json本地文件
# class FangPipeline:
#     def __init__(self):
#         self.newhouse_fp = open("newhouse.json",'wb')
#         self.esfhouse_fp = open("esfhouse.json",'wb')
#         self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp,ensure_ascii=False)
#         self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_fp,ensure_ascii=False)
#
#     def process_item(self, item, spider):
#         self.newhouse_exporter.export_item(item)
#         self.esfhouse_exporter.export_item(item)
#         return item
#
#     def close_spider(self,spider):
#         self.newhouse_fp.close()
#         self.esfhouse_fp.close()

