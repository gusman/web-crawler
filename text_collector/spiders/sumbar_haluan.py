import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class HarianHaluanSpider(CrawlSpider):
    stop_flag = False
    name = "sumbar_haluan"
    allowed_domains = [ 'harianhaluan.com' ]
    start_urls = [
        'https://www.harianhaluan.com/news',
    ]
   
    rules = (
        Rule(
            LinkExtractor(
                allow=('news/detail', )
            ), 
            callback='parse_detail'
        ),
        Rule(
            LinkExtractor(
                    allow=('news/kanal', ),
                    deny=('news/sub', 'news/indeks', 'news/popular')
            ),
        )
    )

    def parse_detail(self, response):
        item = ItemNews()
        item['date'] = response.xpath('//div[@class="date fl"]/text()').get()
        item['title'] = response.xpath('//h1[@class="l_blue2_detik lbold"]/text()').get()
        content = response.xpath('//div[@itemprop="articleBody"]/p/text()').getall()
        item['content']  = "".join(content)
        yield item
