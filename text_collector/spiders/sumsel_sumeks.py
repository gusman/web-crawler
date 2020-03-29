import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class SumselSumeksSpider(CrawlSpider):
    name = 'sumsel_sumeks'
    allowed_domains = [ 'sumeks.co' ]
    start_urls = [
        'https://sumeks.co',
    ]
   
    rules = (
       Rule(
            LinkExtractor(
                allow=('baca'),
            ),
        ),
       Rule(
            LinkExtractor(
                allow=('.', ),
                deny=('foto', 'video', 'dahlan-iskan', 'redaksional-sumeks-co'),
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="entry-title"]//text()').get() 
        item['date'] = response.xpath('//time[@class="updated"]/@datetime').get()
        content = response.xpath('//div[@class="entry-content entry-content-single"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
