import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class JogjaRadarSpider(CrawlSpider):
    name = 'jogja_radar'
    allowed_domains = [ 'radarjogja.co' ]
    start_urls = [
        'https://radarjogja.co',
    ]
   
    rules = (
       Rule(
            LinkExtractor(
                allow=('category'),
            ),
        ),
       Rule(
            LinkExtractor(
                allow=('[0-9]{4}/[0-9]{2}', )
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').get() 
        item['date'] = response.xpath('//time[@itemprop="dateModified"]/@datetime').get()
        content = response.xpath('//div[@itemprop="articleBody"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
