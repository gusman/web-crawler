import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class BatamPosSpider(CrawlSpider):
    name = 'ntb_suara'
    allowed_domains = [ 'suarantb.com' ]
    start_urls = [
        'https://www.suarantb.com',
    ]
   
    rules = (
       Rule(
            LinkExtractor(
                allow=('category'),
            ),
        ),
       Rule(
            LinkExtractor(
                allow=('.', ),
                deny=('store', 'pasang-iklan', 'berlangganan', 'register'),
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('.//h1[@class="entry-title"]//text()').get() 
        item['date'] = response.xpath('.//time[@class="entry-date updated td-module-date"]/@datetime').get()
        content = response.xpath('//div[@class="td-post-content tagdiv-type"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
