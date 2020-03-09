import scrapy
import string

class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
#    url = scrapy.Field()

class BengkuluExpressSpider(scrapy.Spider):
    max_page = 609
    cur_page = 1
    page_url = 'https://bengkuluekspress.com/index/page/'

    name = "bengkulu_express"
    allowed_domains = [ 'bengkuluekspress.com' ]
    start_urls = [
        'https://bengkuluekspress.com/index/',
        #'https://bengkuluekspress.com/index/page/609'
    ]
    
    def parse(self, response):
        """ Retrieve article list """
        self.logger.info('>> PROCESSING in parse %s\n', response.url)
        for link in response.xpath('//div[@class="newser-news active"]//h5[@class="post-title"]/a/@href').getall():
            #self.logger.info('>> link in indekx page %s\n', link)
            yield scrapy.Request(link, callback=self.parse_article_page)

        self.cur_page = self.cur_page + 1
        if self.cur_page <= self.max_page :
            next_url = self.page_url + str(self.cur_page)
            self.logger.info(">>> NEXT URL: %s ", next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_article_page(self, response):
        self.logger.info('>> PROCESSING in parse_article_page %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="post-title"]/text()').get()
        item['date'] = response.xpath('//li[@class="post-date"]/@content').get()
        content = response.xpath('//div[@class="entry-summary"]//p//text()').getall()
        item['content']  = "".join(content)
        #item['url']  = response.url
        yield item
 
