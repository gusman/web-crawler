import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class PapuaJubiSpider(CrawlSpider):
    name = 'papua_jubi'
    allowed_domains = [ 'tabloidjubi.com' ]
    start_urls = [
        'https://tabloidjubi.com',
    ]
   
    rules = (
       Rule(
            LinkExtractor(
                allow=('kategori'),
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
        item['title'] = response.xpath('.//h1[@class="elementor-heading-title elementor-size-default"]//text()').get() 
        item['date'] = response.xpath('.//span[@class="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date"]/text()').get()
        content = response.xpath('//div[@class="elementor-widget-container"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
