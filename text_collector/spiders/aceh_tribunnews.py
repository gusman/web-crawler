import scrapy
import datetime
from datetime import timedelta
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class TribunAcehSpider(scrapy.Spider):
    stop_flag = False
    name = "aceh_tribun"
    allowed_domains = [ 'aceh.tribunnews.com' ]
    start_urls = [
        #'https://aceh.tribunnews.com',
        'https://aceh.tribunnews.com/indeks',
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
            news_urls = response.xpath('//ul[@class="lsi"]/li[@class="ptb15"]//a/@href');
            for news_url in news_urls:
                """ Get news url """
                self.logger.info('\n >> PROCESSING in parse_detail %s\n', response.url)
                url = news_url.get()
                yield scrapy.Request(url, callback=self.parse_news_page)

            self.logger.info('\n >> next url : %s\n', next_url)
            if None == next_url:
                """ Get previous date """
                curr_date = datetime.datetime(int(date_y), int(date_m), int(date_d))
                prev_date = curr_date - timedelta(days = 1) 
                prev_date_str = prev_date.strftime("%Y-%m-%d")
                self.logger.info('\n >> Retrieved date %s-%s-%s\n', date_y, date_m, date_d)
                self.logger.info('\n >> Previous date %s\n', prev_date_str)
                next_url = "https://aceh.tribunnews.com/index-news?date=" + prev_date_str
                yield scrapy.Request(next_url, callback=self.parse)
            else:
                yield scrapy.Request(next_url, callback=self.parse)
    
    def parse_news_page(self, response):
        self.logger.info('\n >> PROCESSING in parse_news_page %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="f50 black2 f400 crimson"]/text()').get()
        item['date'] = response.xpath('//time/text()').get()
        content = response.xpath('//div[@class="side-article txt-article"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
