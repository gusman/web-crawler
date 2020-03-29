import scrapy
import datetime
import re
from datetime import timedelta
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class SultengRayaSpider(scrapy.Spider):
    max_empty = 3
    counter_empty = 0
    handle_httpstatus_list = [404]
    name = "sulteng_raya"
    allowed_domains = [ 'sultengraya.com' ]
    page_url = 'https://sultengraya.com/'
    start_urls = [
        'https://sultengraya.com/2020/03/28/'
    ]

    def get_date_from_url(self, url):
        result = re.search('[0-9]{4}\/[0-9]{2}\/[0-9]{2}', url)
        self.logger.info('\n >> date text: %s\n', result.group(0))
        l_str = result.group(0).split('/')
        return str(l_str[0]), str(l_str[1]), str(l_str[2])

    def parse(self, response):
        """ Retrieve article list """
        self.logger.info('\n >> PROCESSING in parse %s\n', response.url)
        n_news = len(response.xpath('//div[@class="content-column"]//article'))
        next_url = response.xpath('//div[@class="content-column"]//a[@rel="next"]/@href').get()
        date_y, date_m, date_d = self.get_date_from_url(response.url)

        self.logger.info('\n >> n_news : %d\n', n_news)
        self.logger.info('\n >> %s, %s, %s\n', date_y, date_m, date_d)
        if 0 < n_news:
            self.counter_empty = 0
            """ Scrap all news list """
            news_urls = response.xpath('//div[@class="content-column"]//article//h2/a/@href');
            for news_url in news_urls:
                """ Get news url """
                url = news_url.get()
                self.logger.info('\n >> PROCESSING in scrapy request %s\n', url)
                yield scrapy.Request(url, callback=self.parse_news_page)
        else:
            self.logger.info("\n >> Found empty page, counter_empty: %d\n", self.counter_empty)
            self.counter_empty += 1
        
        if 3 > self.counter_empty:
            self.logger.info('\n >> next url : %s\n', next_url)
            if None == next_url:
                """ Get previous date """
                curr_date = datetime.datetime(int(date_y), int(date_m), int(date_d))
                prev_date = curr_date - timedelta(days = 1) 
                prev_date_str = prev_date.strftime("%Y/%m/%d")
                self.logger.info('\n >> Retrieved date %s/%s/%s\n', date_y, date_m, date_d)
                self.logger.info('\n >> Previous date %s\n', prev_date_str)
                next_url = self.page_url + prev_date_str
                self.logger.info('\n >> PROCESSING in scrapy request %s\n', next_url)
                yield scrapy.Request(next_url, callback=self.parse)
            else:
                yield scrapy.Request(next_url, callback=self.parse)
        else:
            self.logger.info("\n >> Reach end of index page : counter_empty: %d\n", self.counter_empty)

    def parse_news_page(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="single-post-title"]//span/text()').get() 
        item['date'] = response.xpath('//time[@class="post-published updated"]/@datetime').get()
        content = response.xpath('//div[@class="entry-content clearfix single-post-content"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
