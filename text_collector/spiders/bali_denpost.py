import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class DenpostSpider(CrawlSpider):
    stop_flag = False
    name = "bali_denpost"
    allowed_domains = [ 'denpost.id' ]
    start_urls = [
        'https://denpost.id/',
    ]
   
    rules = (
        Rule(
            LinkExtractor(
                allow=('[0-9]{4}/[0-9]{2}', )
            ), 
            callback='parse_detail'
        ),
        Rule(
            LinkExtractor(
                    #allow=('category', 'tag', 'page'),
                    deny=('iklan-kolom', 'info-denpost', 'iklan', \
                        'pedoman-media-siber'),
            ),
        )
    )

    def parse_detail(self, response):
        self.logger.info('\n >> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').get()
        item['date'] = response.xpath('//time[@class="entry-date updated td-module-date"]/@datetime').get()
        content = response.xpath('//article//*/p//text()').getall()
        item['content']  = "".join(content)
        yield item
