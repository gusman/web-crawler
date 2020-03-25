import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class KalutMetrokaltaraSpider(CrawlSpider):
    name = 'kalut_metrokaltara'
    allowed_domains = [ 'metrokaltara.com' ]
    start_urls = [
        'https://www.metrokaltara.com',
    ]
   
    rules = (
       Rule(
            LinkExtractor(
                allow=('category'),
                deny=('redaksi', 'contact-us', 'blog', 'category/videos', 'category/video'),
            ),
        ),
       Rule(
            LinkExtractor(
                allow=('.', ),
                deny=('redaksi', 'contact-us', 'blog', 'category/videos', 'category/video'),
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="post-title single-post-title entry-title"]/text()').get()
        item['date'] = response.xpath('//time[@class="entry-date published"]/@datetime').get()
        content = response.xpath('//div[@id="penci-post-entry-inner"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item

