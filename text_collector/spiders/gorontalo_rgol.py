import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class GorontaloRgolSpider(CrawlSpider):
    name = "gorontalo_rgol"
    allowed_domains = [ 'rgol.id' ]
    start_urls = [
        'https://rgol.id',
    ]
   
    rules = (
       Rule(
            LinkExtractor(
                allow=('category', 'topic'),
                deny=('category/dis-way', 'author' ),
            ),
        ),
       Rule(
            LinkExtractor(
                allow=('.', )
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').get()
        item['date'] = response.xpath('//time[@class="updated"]/@datetime').get()
        content = response.xpath('//div[@class="entry-content entry-content-single"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
