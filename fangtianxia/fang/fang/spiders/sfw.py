import scrapy
import re
from fang.items import NewHouseItem,rsfItem
from scrapy_redis.spiders import RedisSpider

class SfwSpider(RedisSpider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    # start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = 'fang:start_urls'

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            # province_text = re.sub(r'/s','',province_text)
            province_text = province_text.strip()
            if province_text:  #这里表示有数据，部分td标签中没有省份
                province = province_text
            if province == "其它":
                continue
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                try:
                    city_urllist = city_url.split(".")
                    firstpart = city_urllist[0]
                    secodepart = city_urllist[1]
                    thirdpart = city_urllist[2]
                except Exception as e:
                    print(e)
                    print("生成城市URL失败")
                # 构建新房链接
                new_city_url = firstpart + ".newhouse." + secodepart + '.' + thirdpart + "house/s/"
                # 构建二手房链接
                esf_city_url = firstpart + ".esf." + secodepart + '.' + thirdpart
                print("城市：%s %s"%(province,city))
                print("新房链接：%s" %new_city_url)
                print("二手房链接：%s" %esf_city_url)
                # 进行新房页面解析
                yield scrapy.Request(url=new_city_url,callback=self.parse_newhouse,meta={'info':(province,city,new_city_url)})
                # 进行二手房页面解析
                yield scrapy.Request(url=esf_city_url,callback=self.parse_esfhouse,meta={'info':(province,city,esf_city_url)})
    def parse_newhouse(self,response):
        province,city,new_city_url = response.meta.get("info")
        lis = response.xpath("//div[contains(@class,'nl_con')]/ul//li")
        # lis = lis[0::]
        for li in lis:
            name = li.xpath(".//div[@class='nlcd_name']/a/text()").get()
            if name:
                name = name.strip()
            elif not name:
                continue
            house_type_list = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
            area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall()).strip()
            area = re.sub(r'\s|/|－','',area)
            address = li.xpath(".//div[@class='address']/a/@title").get()
            try:
                district = re.search(r'.*(\[.*?\]).*', address).group(1)
            except Exception as e:
                print("行政区获取失败",e)
                district = ''
            sale = li.xpath(".//div[@class='fangyuan']/span/text()").get()
            price_number = li.xpath(".//div[@class='nhouse_price']/span/text()").get()
            price_info = li.xpath(".//div[@class='nhouse_price']/em/text()").get()
            print("房子价格信息为",price_number,price_info)
            try:
                price = price_number + price_info
            except Exception as e:
                print("当前价格不完善",e)
                price = "价格待定"
            origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()
            origin_url = "https:"+origin_url

            item = NewHouseItem(province=province,city=city,name=name,price=price,rooms=house_type_list,area=area,address=address, \
                                district=district,sale=sale,origin_url=origin_url)
            print("小区名字",name,"小区住宅类型",house_type_list,"房子面积",area,"地址为",address,"行政区为",\
                  district,"是否在售", sale,"房子价格信息为",price)
            yield item
        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        if next_url:
            next_url = new_city_url+next_url
            yield scrapy.Request(url=next_url,callback=self.parse_newhouse,meta={'info':(province,city,new_city_url)})


    def parse_esfhouse(self,response):
        province,city,esf_city_url= response.meta.get("info")
        dls = response.xpath("//div[contains(@class,'shop_list')]//dl")
        for dl in dls:
            name = dl.xpath(".//p[@class='add_shop']/a/text()").get()
            if not name:
                continue
            name = name.strip()
            try:
                roomsinfo = "".join(dl.xpath(".//p[@class='tel_shop']//text()").getall()).strip()
                roomsinfo = re.sub(r'\s','',roomsinfo)[0::].split("|")
                rooms = roomsinfo[0]
                area = roomsinfo[1]
                floor = roomsinfo[2]
                toward = roomsinfo[3]
                year = roomsinfo[4]
            except Exception as e:
                print("获取房子类型出错，错误类型为",e)
                year = ""
            address = dl.xpath(".//p[@class='add_shop']/span/text()").get()
            if not address:
                continue
            address = address.strip()
            unit = "".join(dl.xpath(".//span[@class='red']//text()").getall()).strip()
            price = dl.xpath(".//dd[@class='price_right']//span[not(@class)]/text()").get()
            origin_url = dl.xpath(".//h4[@class='clearfix']/a/@href").get()
            if origin_url:
                origin_url = esf_city_url+origin_url
            item = rsfItem(province=province,city=city,name=name,rooms=rooms,floor=floor,toward=toward,\
                           address=address,year=year,area=area,price=price,unit=unit,origin_url=origin_url)
            print("小区名字",name,"房子类型",rooms,"房子面积",area,"房子层数",floor,"房子朝向",toward,"房子年代",year,\
                  "房子详细地址",address,"房子单价",price,"房子总价",unit,"房子链接地址",origin_url)
            yield item
        next_url = response.xpath("//div[@class='page_al']/p/a/@href").get()
        if next_url:
            next_url = esf_city_url+next_url
            yield scrapy.Request(url=next_url,callback=self.parse_esfhouse,meta={"info":(province,city,esf_city_url)})
