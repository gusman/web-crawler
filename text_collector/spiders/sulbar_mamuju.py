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

class SulbarMamujuSpider(scrapy.Spider):
    name = "sulbar_mamuju"
    allowed_domains = [ 'mamujupos.com' ]
    page_url = 'https://mamujupos.com/'
    start_urls = [
        'https://mamujupos.com/2020/03/27'
    ]


    def get_date_from_url(self, url):
        result = re.search('[0-9]{4}\/[0-9]{2}\/[0-9]{2}', url)
        self.logger.info('\n >> date text: %s\n', result.group(0))
        l_str = result.group(0).split('/')
        return str(l_str[0]), str(l_str[1]), str(l_str[2])


    def parse(self, response):
        """ Retrieve article list """
        self.logger.info('\n >> PROCESSING in parse %s\n', response.url)
        n_news = len(response.xpath('//section[@class="widget archive"]//div[@class="excrp"]'))
        next_url = response.xpath('//a[contains(text(), "Berikutnya") and @class="next page-numbers"]/@href').get()
        date_y, date_m, date_d = self.get_date_from_url(response.url)

        self.logger.info('\n >> n_news : %d\n', n_news)
        self.logger.info('\n >> %s, %s, %s\n', date_y, date_m, date_d)
        if 0 < n_news:
            """ Scrap all news lsit """
            news_urls = response.xpath('//section[@class="widget archive"]//div[@class="excrp"]//a/@href');
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
                prev_date_str = prev_date.strftime("%Y/%m/%d")
                self.logger.info('\n >> Retrieved date %s/%s/%s\n', date_y, date_m, date_d)
                self.logger.info('\n >> Previous date %s\n', prev_date_str)
                next_url = self.page_url + prev_date_str
                self.logger.info('\n >> PROCESSING in scrapy request %s\n', next_url)
                yield scrapy.Request(next_url, callback=self.parse)
            else:
                yield scrapy.Request(next_url, callback=self.parse)

    def parse_news_page(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('.//article[@class="ispost"]/h2/text()').get() 
        item['date'] = response.xpath('.//li[@class="dte"]/text()').get()
        content = response.xpath('//div[@class="entry"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item