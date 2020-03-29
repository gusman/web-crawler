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

class SultraZonaSpider(scrapy.Spider):
    max_empty = 3
    counter_empty = 0
    name = "sumut_go"
    allowed_domains = [ 'gosumut.com' ]
    start_urls = [
        'https://www.gosumut.com/news-index/?indexDate=29&indexMonth=03&indexYear=2020&Submit=Tampilkan'
#        'https://www.gosumut.com/news-index/?indexDate=20&indexMonth=11&indexYear=2015&Submit=Tampilkan'
    ]

    def get_date_from_url(self, url):
        result = re.search('indexDate=[0-9]{2}', url)
        result = re.search('[0-9]{2}', result.group(0))
        date_d = result.group(0)

        result = re.search('indexMonth=[0-9]{2}', url)
        result = re.search('[0-9]{2}', result.group(0))
        date_m = result.group(0)

        result = re.search('indexYear=[0-9]{4}', url)
        result = re.search('[0-9]{4}', result.group(0))
        date_y = result.group(0)

        self.logger.info('\n >> date text: [%s/%s/%s]\n', date_y, date_m, date_d)
        return date_y, date_m, date_d


    def construct_page_url_by_date(self, date_str):
        l_str = date_str.split('/')
        date_y, date_m, date_d = str(l_str[0]), str(l_str[1]), str(l_str[2])
        url = "https://www.gosumut.com/news-index/?indexDate=" + date_d + "&indexMonth=" + date_m + "&indexYear=" + date_y + "&Submit=Tampilkan"
        return url

    def parse(self, response):
        """ Retrieve article list """
        self.logger.info('\n >> PROCESSING in parse %s\n', response.url)
        n_news = len(response.xpath('//div[@class="newslist"]//a'))
        #next_url = response.xpath('//i[@class="td-icon-menu-right"]/ancestor::a/@href').get()
        next_url = None
        date_y, date_m, date_d = self.get_date_from_url(response.url)

        self.logger.info('\n >> n_news : %d\n', n_news)
        self.logger.info('\n >> %s, %s, %s\n', date_y, date_m, date_d)
        if 0 < n_news:
            self.counter_empty = 1
            """ Scrap all news list """
            news_urls = response.xpath('//div[@class="newslist"]//a/@href');
            for news_url in news_urls:
                """ Get news url """
                url = news_url.get()
                url = "https://www.gosumut.com" + url
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
        item['title'] = response.xpath('//div[@class="news-box-view" and @itemprop="articleBody"]/h1/text()').get() 
        item['date'] = response.xpath('//div[@class="time"]/text()').get().strip()
        content = response.xpath('//div[@class="news-content"]//text()[parent::p or parent::strong or parent::div[@class="news-box-desc-right"]]').getall()
        content = [ c.strip() for c in content if 0 < len(c.strip()) ]
        content = [ c.replace("\r\n", " ") for c in content ]
        content = [ c.replace("\n", " ") for c in content ]
        item['content']  = "".join(content)
        yield item
