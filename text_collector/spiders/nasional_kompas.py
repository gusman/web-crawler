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

class NasionalKompasSpider(scrapy.Spider):
    max_empty = 5 
    counter_empty = 0
    handle_httpstatus_list = [404]
    name = "nasional_kompas"
    allowed_domains = [ 'kompas.com' ]
    start_urls = [
        'https://indeks.kompas.com/?site=all&date=2020-03-31&page=1'
        #'https://money.kompas.com/read/2020/03/31/113546426/ada-virus-corona-seberapa-banyak-dana-darurat-yang-harus-dimiliki'
    ]

    def get_date_from_url(self, url):
        result = re.search('[0-9]{4}\-[0-9]{2}\-[0-9]{2}', url)
        self.logger.info('\n >> date text: %s\n', result.group(0))
        l_str = result.group(0).split('-')
        return str(l_str[0]), str(l_str[1]), str(l_str[2])
    
    def construct_page_url_by_date(self, date_str):
        url = "https://indeks.kompas.com/?site=all&date=" + date_str
        return url

    def parse(self, response):
        """ Retrieve article list """
        self.logger.info('\n >> PROCESSING in parse %s\n', response.url)
        n_news = len(response.xpath('//div[@class="article__asset"]/a'))
        next_url = response.xpath('//a[@class="paging__link paging__link--next" and @rel="next"]/@href').get()
        date_y, date_m, date_d = self.get_date_from_url(response.url)

        self.logger.info('\n >> n_news : %d\n', n_news)
        self.logger.info('\n >> %s, %s, %s\n', date_y, date_m, date_d)
        if 0 < n_news:
            self.counter_empty = 0
            """ Scrap all news list """
            news_urls = response.xpath('//div[@class="article__asset"]/a/@href');
            for news_url in news_urls:
                """ Get news url """
                url = news_url.get()
                self.logger.info('\n >> PROCESSING in scrapy request %s\n', url)
                yield scrapy.Request(url, callback=self.parse_news_page)
        else:
            self.logger.info("\n >> Found empty page, url: %s, counter_empty: %d\n", response.url, self.counter_empty)
            self.counter_empty += 1
        
        if self.max_empty > self.counter_empty:
            self.logger.info('\n >> next url : %s\n', next_url)
            if None == next_url:
                """ Get previous date """
                curr_date = datetime.datetime(int(date_y), int(date_m), int(date_d))
                prev_date = curr_date - timedelta(days = 1) 
                prev_date_str = prev_date.strftime("%Y-%m-%d")
                self.logger.info('\n >> Retrieved date %s-%s-%s\n', date_y, date_m, date_d)
                self.logger.info('\n >> Previous date %s\n', prev_date_str)
                next_url = self.construct_page_url_by_date(prev_date_str)
                self.logger.info('\n >> PROCESSING in scrapy request %s\n', next_url)
                yield scrapy.Request(next_url, callback=self.parse)
            else:
                yield scrapy.Request(next_url, callback=self.parse)
        else:
            self.logger.info("\n >> Reach end of index page : counter_empty: %d\n", self.counter_empty)

    def parse_news_page(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="read__title"]//text()').get()
        item['date'] = response.xpath('//div[@class="read__time"]/text()').get()
        content = response.xpath('//div[@class="read__content"]//text()[parent::p or parent::h2 or parent::a or parent::strong or parent::h3]').getall()
        item['content']  = "".join(content)
        yield item

        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_news_page)

