import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class JabarKpolSpider(CrawlSpider):
    name = 'jabar_kapol'
    allowed_domains = [ 'kapol.id' ]
    start_urls = [
        'https://kapol.id',
    ]
   
    rules = (
       Rule(
            LinkExtractor(
                allow=('topik'),
            ),
        ),
       Rule(
            LinkExtractor(
                allow=('.', ),
                deny=('topik/kuliner', 'topik/hiburan'),
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="mvp-post-title left entry-title" and @itemprop="headline"]/text()').get()
        item['date'] = response.xpath('//time[@class="post-date updated"]/@datetime').get()
        content = response.xpath('//div[@class="theiaPostSlider_preloadedSlide"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
