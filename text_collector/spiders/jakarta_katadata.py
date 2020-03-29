import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class JakartaKatadataSpider(scrapy.Spider):
    max_page = 47240
    cur_page = 0
    page_url = 'https://katadata.co.id/indeks/listing/'

    name = 'jakarta_katadata'
    allowed_domains = [ 'katadata.co.id' ]
    start_urls = [
        'https://katadata.co.id/indeks/listing/',
    ]
   

    def parse(self, response):
        """ Retrieve article list """
        self.logger.info('>> PROCESSING in parse %s\n', response.url)
        for link in response.xpath('//h2[@class="title-indeks"]/a/@href').getall():
            self.logger.info('>> link in indeks page %s\n', link)
            yield scrapy.Request(link, callback=self.parse_article_page)

        self.cur_page = self.cur_page + 10
        if self.cur_page <= self.max_page :
            next_url = self.page_url + str(self.cur_page)
            self.logger.info(">>> NEXT URL: %s ", next_url)
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_article_page(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        title = response.xpath('//h1[@class="width-65 xs-width-auto"]//text()').getall() 
        title = [ t.strip() for t in title if 0 < len(t.strip()) ]
        item['title'] = "".join(title)
        item['date'] = response.xpath('//text()[parent::date]').get()
        content = response.xpath('//article[@class="textArticle" and @itemprop="articleBody"]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
