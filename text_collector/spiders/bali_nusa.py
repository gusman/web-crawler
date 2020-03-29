import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class BaliNusaSpider(CrawlSpider):
    name = 'bali_nusa'
    allowed_domains = [ 'nusabali.com' ]
    start_urls = [
        'https://www.nusabali.com',
    ]
   
    rules = (
       Rule(
            LinkExtractor(
                allow=('regional', 'kategori'),
            ),
        ),
       Rule(
            LinkExtractor(
                allow=('berita', ),
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//span[@itemprop="headline"]/text()').get() 
        item['date'] = response.xpath('//span[@class="month pull-left" and @itemprop="datePublished"]/text()').get()
        content = response.xpath('//div[@class="row"]//div[@class="entry-content"]//text()[parent::p or parent::div] ').getall()
        content = [ c.strip() for c in content if 0 < len(c.strip()) ]
        content = [ c.replace("\r\n", " ") for c in content ]
        content = [ c.replace("\n", " ") for c in content ]
        item['content']  = "".join(content)
        yield item
