import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import JianshuSpiderItem

class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detial', follow=True),
    )

    def parse_detial(self, response):
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        content = response.xpath("//article[@class='_2rhmJa']").getall()
        author = response.xpath("//span[@class='_22gUMi']/text()").get()
        # avatar = response.xpath("//div[@class='_2mYfmT']/a[@class='_1OhGeD']/img/@src").get()
        url1 = response.url
        url = url1.split("?")[0]
        article_id = url.split('/')[-1]
        origin_url = url1
        avatar = response.xpath("//a[@class='_1OhGeD']/img/@src").get()
        pub_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        read_count = response.xpath("//div[@class='s-dsoj']/span[last()]/text()").get()
        word_count = response.xpath("//div[@class='s-dsoj']/span[1]/text()").get()
        try:
            read_count = read_count[2:].replace(',', '')
            word_count = word_count[2:].replace(',', '')
        except:
            read_count = 0
            word_count = 0
        subjects = ','.join(response.xpath("//div[@class='_2Nttfz']/a/span/text()").getall())
        # avatar = scrapy.Field()
        # pub_time = scrapy.Field()
        # read_count = scrapy.Field()
        # word_count = scrapy.Field()
        # subjects = scrapy.Field()
        item = JianshuSpiderItem(
            title=title,
            content=content,
            author=author,
            article_id=article_id,
            origin_url=origin_url,
            avatar=avatar,
            pub_time=pub_time,
            read_count=read_count,
            word_count=word_count,
            subjects=subjects
        )
        yield item
        # put_time = response.xpath("//div[@class='s-dsoj']//time/text()").get()


