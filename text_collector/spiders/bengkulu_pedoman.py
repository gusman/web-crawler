import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class BengkuluPedomanSpider(CrawlSpider):
    handle_httpstatus_list = [404]
    stop_flag = False
    name = "bengkulu_pedoman"
    allowed_domains = [ 'pedomanbengkulu.com' ]
    start_urls = [
        'http://pedomanbengkulu.com/',
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
                allow=('category'),
                deny=('oase', 'opini', 'jelajah')
            ),
        ),
    )

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'ROBOTSTXT_OBEY': False
    }

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').get()
        item['date'] = response.xpath('//time[@class="entry-date updated td-module-date"]/@datetime').get()
        content = response.xpath('//div[@class="td-post-content"]/p//text()').getall()
        item['content']  = "".join(content)
        yield item
