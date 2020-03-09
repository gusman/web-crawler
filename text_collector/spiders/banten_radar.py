import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class RaderBantenSpider(CrawlSpider):
    stop_flag = False
    name = "banten_radar"
    allowed_domains = [ 'radarbanten.co.id' ]
    start_urls = [
        'https://www.radarbanten.co.id',
    ]
   
    rules = (
        Rule(
            LinkExtractor(
                allow=('category'),
                deny=('dahlan-iskan', 'seleb', 'radar-foto', 'otomotif', 
                    'pedoman-pemberitaan-media-siber' ),
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
        item['date'] = response.xpath('//time[@class="entry-date updated td-module-date"]/@datetime').get()
        content = response.xpath('//div[@class="td-post-content"]/p//text()').getall()
        item['content']  = "".join(content)
        yield item
