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
#    url = scrapy.Field()

class TribunJatengSpider(scrapy.Spider):
    name = "nasional_sindo"
    allowed_domains = [ 'sindonews.com' ]
    page_url = 'https://index.sindonews.com/index/0?t='
    start_urls = [
        'https://index.sindonews.com/index/0?t=2020-03-15'
    ]

    def get_date_from_url(self, url):
        result = re.search('[0-9]{4}\-[0-9]{2}\-[0-9]{2}', url)
        if None != result:
            self.logger.info('\n >> date text: %s\n', result.group(0))
            l_str = result.group(0).split('-')
            return {
                    'year'  : l_str[0],
                    'month' : l_str[1],
                    'day'   : l_str[2] }

    def parse(self, response):
        """ Retrieve article list """
        self.logger.info('\n >> PROCESSING in parse %s\n', response.url)
        n_news = len(response.xpath('//div[@class="indeks-news"]'))
        next_url = response.xpath('//a[@rel="next"]/@href').get()
       
        """ retrieve date from url """
        dict_date = self.get_date_from_url(response.url)
        date_y = dict_date['year']
        date_m = dict_date['month']
        date_d = dict_date['day']

        self.logger.info('\n >> n_news : %d\n', n_news)
        
        if 0 < n_news:
            """ Scrap all news lsit """
            news_urls = response.xpath('//div[@class="indeks-news"]//div[@class="indeks-title"]/a/@href');
            for news_url in news_urls:
                """ Get news url """
                url = news_url.get()
                self.logger.info('\n >> PROCESSING in scrapy request %s\n', url)
                yield scrapy.Request(url, callback=self.parse_news_page)

            self.logger.info('\n >> next url : %s\n', next_url)
            if None == next_url:
                """ Get previous date """
                self.logger.info('\n >> Y-m-d, %d-%d-%d', int(date_y), int(date_m), int(date_d))
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
        item['title'] = response.xpath('//div[@class="article"]/h1/text()').get()
        item['date'] = response.xpath('//time/text()').get()
        content = response.xpath('//div[@class="article"]\
                //div[@id="content"]\
                //text()[not(ancestor::a) and not(ancestor::div/@class = "baca-inline-head")]').getall()
        item['content']  = "".join(content)
        #item['url']  = response.url
        yield item
        
        #next_url = response.xpath('//div[@class="mb20"]/a/@href').get()
        #self.logger.info('\n >> PROCESSING in parse_news_page, next_url %s\n', next_url)
        #if None != next_url:
        #    yield scrapy.Request(next_url, callback=self.parse_news_page)

