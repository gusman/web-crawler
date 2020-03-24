import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class KaltengTabenganSpider(CrawlSpider):
    name = 'kalteng_tabengan'
    allowed_domains = [ 'tabengan.com' ]
    start_urls = [
        'https://www.tabengan.com/',
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
                deny=('redaksi', 'hubungi-kami', 'tentang-kami', 'pedoman-pemberitaan-media-siber'),
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="jeg_post_title"]/text()').get()
        item['date'] = response.xpath('//div[@class="jeg_meta_date"]/a/text()').get()
        content = response.xpath('//div[@class="content-inner "]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
