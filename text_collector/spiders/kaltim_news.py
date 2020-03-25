import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class KaltimNewsBanuaSpider(CrawlSpider):
    name = 'kaltim_news'
    allowed_domains = [ 'newskaltim.com' ]
    start_urls = [
        'https://newskaltim.com',
        #'https://newskaltim.com/18-kasus-corona-di-ppu-tertangani/'
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
                deny=('redaksi', 'contact-us', 'blog'),
            ), 
            callback='parse_detail'
        ),
    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        for article in response.xpath('//article[@id="post-area"]'):
            item = ItemNews()
            item['title'] = article.xpath('.//h1[@itemprop="headline"]//text()').get() 
            item['date'] = article.xpath('.//time[@class="post-last-modified-td"]/text()').get()
            content = response.xpath('//div[@id="content-main"]//p//text()').getall()
            item['content']  = "".join(content)
            yield item

#        item = ItemNews()
#        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').get()
#        item['date'] = response.xpath('//time[@class="entry-date updated td-module-date"]/@datetime').get()
#        content = response.xpath('//div[@class="td-post-content"]//p//text()').getall()
#        item['content']  = "".join(content)
#        yield item

