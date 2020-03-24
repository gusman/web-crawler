import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class KaltengTribunSpider(CrawlSpider):
    name = 'kalteng_tribun'
    allowed_domains = [ 'kalteng.tribunnews.com' ]
    start_urls = [
        'https://kalteng.tribunnews.com'
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
                allow=('.',),
            ),
        )

    )

    def parse_detail(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()

        item['title'] = response.xpath('//h1[@id="arttitle"]//text()').get()
        item['date'] = response.xpath('//time/text()').get()
        content = response.xpath('//div[@class="side-article txt-article"]//p//text()').getall()
        item['content']  = "".join(content)
        #item['url']  = response.url
        yield item
        
        next_url = response.xpath('//div[@class="mb20"]/a/@href').get()
        self.logger.info('\n >> PROCESSING in parse_news_page, next_url %s\n', next_url)
        if None != next_url:
            yield scrapy.Request(next_url, callback=self.parse_detail)
