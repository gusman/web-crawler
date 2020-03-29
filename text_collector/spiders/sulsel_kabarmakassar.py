import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class SulselKabarMakasarSpider(CrawlSpider):
    name = 'sulsel_kabarmakassar'
    allowed_domains = [ 'kabarmakassar.com' ]
    start_urls = [
        'https://www.kabarmakassar.com/',
    ]
   
    rules = (
       Rule(
            LinkExtractor(
                allow=('category', 'tag', '[0-9]{4}\/[0-9]{2}'),
            ),
        ),
       Rule(
            LinkExtractor(
                allow=('.', ),
                deny=('pedoman-media-siber', ),
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('.//h1[@class="elementor-heading-title elementor-size-default"]//text()').get() 
        item['date'] = response.xpath('.//span[@class="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date"]/text()').get()
        content = response.xpath('//div[@id="content"]//div[@class="elementor-widget-container"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
