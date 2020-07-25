# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewHouseItem(scrapy.Item):
    #省份
    province = scrapy.Field()
    #城市
    city = scrapy.Field()
    #小区名字
    name = scrapy.Field()
    #价格
    price = scrapy.Field()
    #几居室
    rooms = scrapy.Field()
    #面积
    area = scrapy.Field()
    #地址
    address = scrapy.Field()
    #行政区
    district = scrapy.Field()
    #是否在售
    sale = scrapy.Field()
    #详情页url
    origin_url = scrapy.Field()

class rsfItem(scrapy.Item):
    #省份
    province = scrapy.Field()
    #城市
    city = scrapy.Field()
    # 小区名字
    name = scrapy.Field()
    # 几居室
    rooms = scrapy.Field()
    # 层
    floor = scrapy.Field()
    # 朝向
    toward = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 年代
    year = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 单价
    price = scrapy.Field()
    # 总价
    unit = scrapy.Field()
#    原始url
    origin_url = scrapy.Field()

