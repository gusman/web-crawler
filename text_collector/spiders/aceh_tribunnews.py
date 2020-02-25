import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class SinggalangSpider(CrawlSpider):
    stop_flag = False
    name = "aceh_tribun"
    allowed_domains = [ 'aceh.tribunnews.com' ]
    start_urls = [
        'https://aceh.tribunnews.com',
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
                    deny=('epaper', ),
            ),
        )
    )

    def parse_detail(self, response):
        #self.logger.info('\n >> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="f50 black2 f400 crimson"]/text()').get()
        item['date'] = response.xpath('//time/text()').get()
        content = response.xpath('//div[@class="side-article txt-article"]//p/text()').getall()
        item['content']  = "".join(content)
        yield item
