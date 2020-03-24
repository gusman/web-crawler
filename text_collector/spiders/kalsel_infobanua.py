import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class KalselInfoBanuaSpider(CrawlSpider):
    name = 'kalsel_infobanua'
    allowed_domains = [ 'infobanua.co.id' ]
    start_urls = [
        'http://infobanua.co.id/',
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
                deny=('redaksi', 'hubungi-kami', 'profil-infobanua-co-id'),
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').get()
        item['date'] = response.xpath('//time[@class="entry-date updated td-module-date"]/@datetime').get()
        content = response.xpath('//div[@class="td-post-content"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
