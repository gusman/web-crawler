import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class JabarPikiranRakyatSpider(CrawlSpider):
    name = 'jabar_pikiranrakyat'
    allowed_domains = [ 'pikiran-rakyat.com' ]
    start_urls = [
        'https://www.pikiran-rakyat.com',
    ]
   
    rules = (
        Rule(
            LinkExtractor(
                allow=('pr-', ),
            ), 
            callback='parse_detail'
        ),
        Rule(
            LinkExtractor(
                allow=('.', ),
            ), 
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="read__title"]//text()').get().strip() 
        date  = response.xpath('//div[@class="read__info__date"]/text()').get().strip()
        item['date'] = date.replace('- ', '')
        content = response.xpath('//article[@class="read__content clearfix"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
