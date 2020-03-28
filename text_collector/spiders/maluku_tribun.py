import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class MalukuTribunSpider(CrawlSpider):
    name = 'maluku_tribun'
    allowed_domains = [ 'tribun-maluku.com' ]
    start_urls = [
        'https://www.tribun-maluku.com',
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
                deny=('redaksi', 'hubungi-kami', 'ketentuan-penggunaan', 'kebijakan-privasi'),
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('.//h1[@class="jeg_post_title"]//text()').get() 
        item['date'] = response.xpath('.//div[@class="jeg_meta_date"]/a/text()').get()
        content = response.xpath('//div[@class="content-inner "]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
