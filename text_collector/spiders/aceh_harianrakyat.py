import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class SinggalangSpider(CrawlSpider):
    stop_flag = False
    name = "aceh_harianrakyat"
    allowed_domains = [ 'harianrakyataceh.com' ]
    start_urls = [
        'https://harianrakyataceh.com/',
    ]
   
    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    '([A-Za-z])\w+\/[0-9]{4}\/[0-9]{2}\/[0-9]{2}', 
                    '/[0-9]{4}\/[0-9]{2}\/[0-9]{2}', 
                )
            ), 
            callback='parse_detail'
        ),
        Rule(
            LinkExtractor(
                allow=('page'),
                deny=('epaper', 'category/photo'),
            ),
        )
    )

    def parse_detail(self, response):
        #self.logger.info('\n >> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').get()
        item['date'] = response.xpath('//time/text()').get()
        content = response.xpath('//article//*/p//text()').getall()
        item['content']  = "".join(content)
        yield item
