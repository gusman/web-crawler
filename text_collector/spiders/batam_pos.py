import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class BatamPosSpider(CrawlSpider):
    name = 'batam_pos'
    allowed_domains = [ 'batampos.co.id' ]
    start_urls = [
        'https://batampos.co.id',
    ]
   
    rules = (
       Rule(
            LinkExtractor(
                allow=('rubrik'),
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
        content = response.xpath('//div[@class="td-post-content td-pb-padding-side"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
