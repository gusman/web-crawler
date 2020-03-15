import scrapy
import datetime
from datetime import timedelta
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
#    url = scrapy.Field()

class TribunJatengSpider(scrapy.Spider):
    name = "surabaya_tribun"
    allowed_domains = [ 'surabaya.tribunnews.com' ]
    page_url = 'https://surabaya.tribunnews.com/index-news?date='
    start_urls = [
        'https://surabaya.tribunnews.com/index-news?date=2020-3-15'
    ]
    
    def parse(self, response):
        """ Retrieve article list """
        self.logger.info('\n >> PROCESSING in parse %s\n', response.url)
        n_news = len(response.xpath('//li[@class="ptb15"]'))
        next_url = response.xpath('//a[text()="Next"]/@href').get()
        date_d = response.xpath('//select[@id="dayindex"]/option[boolean(@selected)]/@value').get()
        date_m = response.xpath('//select[@id="monthindex"]/option[boolean(@selected)]/@value').get()
        date_y = response.xpath('//select[@id="yearindex"]/option[boolean(@selected)]/@value').get()

        self.logger.info('\n >> n_news : %d\n', n_news)
        if 0 < n_news:
            """ Scrap all news lsit """
            news_urls = response.xpath('//ul[@class="lsi"]/li[@class="ptb15"]//h3//a/@href');
            for news_url in news_urls:
                """ Get news url """
                url = news_url.get()
                self.logger.info('\n >> PROCESSING in scrapy request %s\n', url)
                yield scrapy.Request(url, callback=self.parse_news_page)

            self.logger.info('\n >> next url : %s\n', next_url)
            if None == next_url:
                """ Get previous date """
                curr_date = datetime.datetime(int(date_y), int(date_m), int(date_d))
                prev_date = curr_date - timedelta(days = 1) 
                prev_date_str = prev_date.strftime("%Y-%m-%d")
                self.logger.info('\n >> Retrieved date %s-%s-%s\n', date_y, date_m, date_d)
                self.logger.info('\n >> Previous date %s\n', prev_date_str)
                next_url = self.page_url + prev_date_str
                self.logger.info('\n >> PROCESSING in scrapy request %s\n', next_url)
                yield scrapy.Request(next_url, callback=self.parse)
            else:
                yield scrapy.Request(next_url, callback=self.parse)
    
    def parse_news_page(self, response):
        self.logger.info('\n >> PROCESSING in parse_news_page %s\n', response.url)
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
            yield scrapy.Request(next_url, callback=self.parse_news_page)

