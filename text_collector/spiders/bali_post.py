import scrapy
import re
import datetime
from datetime import timedelta
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
#    url = scrapy.Field()

class TribunAcehSpider(scrapy.Spider):
    last_date = '2017/02/25'
    name = "bali_post"
    allowed_domains = [ 'balipost.com' ]
    start_urls = [
        'http://www.balipost.com/news/2020/03/01',
    ]
  
    def __init__(self,  *args, **kwargs):
        self.prev_date = None
        self.last_date_epoch = self.get_epoch_date(self.last_date)
        super().__init__(*args, **kwargs)

    def get_epoch_date(self, date_str):
        l_str = date_str.split('/')
        return datetime.datetime(
                        int(l_str[0]), 
                        int(l_str[1]), 
                        int(l_str[2])).timestamp()

    def get_date_from_url(self, url):
        result = re.search('[0-9]{4}\/[0-9]{2}\/[0-9]{2}', url)
        if None != result:
            self.logger.info('\n >> date text: %s\n', result.group(0))
            l_str = result.group(0).split('/')
            self.prev_date = datetime.datetime(
                        int(l_str[0]), 
                        int(l_str[1]), 
                        int(l_str[2]))
        else:
            self.prev_date = self.prev_date - timedelta(days = 1) 
            prev_date_str = self.prev_date.strftime("%Y/%m/%d")
            l_str = prev_date_str.split('/')
            
        self.logger.info(">>> PREV DATE EPOCH: %s", self.prev_date.timestamp())
        self.logger.info(">>> LAST DATE EPOCH: %s", self.last_date_epoch)
        
        if int(self.prev_date.timestamp()) <= int(self.last_date_epoch):
            return None
        else:
            return {
                    'year'  : l_str[0],
                    'month' : l_str[1],
                    'day'   : l_str[2] }

    def parse(self, response):
        """ Retrieve article list """
        self.logger.info('>> PROCESSING in parse %s', response.url)
        n_news = len(response.xpath('//div[@class="td-block-span6"]'))
        next_url = response.xpath('//a/i[@class="td-icon-menu-right"]/../@href').get()
      
        ar_date = self.get_date_from_url(response.url)
        self.logger.info('>> n_news : %d', n_news)
        if 0 < n_news and None != ar_date:
            """ Scrap all news lsit """
            news_urls = response.xpath('//div[@class="td-block-span6"]//h3//a/@href');
            for news_url in news_urls:
                """ Get news url """
                url = "http:" + news_url.get()
                self.logger.info('>> Scrapy Request [News Content] %s', url)
                #yield scrapy.Request(url, callback=self.parse_news_page)

            self.logger.info('>> next url : %s', next_url)
            if None == next_url or '#' == next_url:
                """ Get previous date """
                curr_date = datetime.datetime(int(ar_date['year']), int(ar_date['month']), int(ar_date['day']))
                prev_date = curr_date - timedelta(days = 1) 
                prev_date_str = prev_date.strftime("%Y/%m/%d")
                self.logger.info('>> Retrieved date %s',str(ar_date))
                self.logger.info('>> Previous date %s', prev_date_str)
                next_url = "http://www.balipost.com/news/" + prev_date_str
                self.logger.info('>> Scrapy request [Previous Date] %s', next_url)
                yield scrapy.Request(next_url, callback=self.parse)
            else:
                next_url = "http:" + next_url
                self.logger.info('>> Scrapy request [Next Page] %s', next_url)
                yield scrapy.Request(next_url, callback=self.parse)
        else:
            self.logger.info('No news and last date')
    
    def parse_news_page(self, response):
        self.logger.info('\n >> PROCESSING in parse_news_page %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="entry-title"]//text()').get()
        item['date'] = response.xpath('//time[@class="entry-date updated td-module-date"]/@datetime').get()
        content = response.xpath('//div[@class="td-post-content"]\
                //*[self::p or self::span or self::h1 or self::h2 or self::h3 or self::h4 or self::h5]\
                //text()').getall()

        item['content']  = "".join(content)
#        #item['url']  = response.url
        yield item
#        
#        next_url = response.xpath('//div[@class="mb20"]/a/@href').get()
#        self.logger.info('\n >> PROCESSING in parse_news_page, next_url %s\n', next_url)
#        if None != next_url:
#            yield scrapy.Request(next_url, callback=self.parse_news_page)
#
