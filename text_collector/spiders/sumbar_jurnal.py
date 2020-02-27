import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class JurnalSumbarSpider(CrawlSpider):
    stop_flag = False
    name = "sumbar_jurnal"
    allowed_domains = [ 'jurnalsumbar.com' ]
    start_urls = [
        'https://jurnalsumbar.com/',
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
                    allow=('category', 'tag', 'page'),
                    deny=('privacy-policy', 'tentang-kami', 'pedoman-media-siber'),
            ),
        )
    )

    def parse_detail(self, response):
        #self.logger.info('\n >> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').get()
        item['date'] = response.xpath('//time[@class="entry-date updated td-module-date"]/text()').get()
        content = response.xpath('//article//p//text()').getall()
        item['content']  = "".join(content)
        yield item
