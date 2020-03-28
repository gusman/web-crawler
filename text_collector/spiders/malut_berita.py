import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class MalutBeritaSpider(scrapy.Spider):
    max_page = 590
    cur_page = 1
    page_url = 'http://beritamalut.co/page/'

    name = 'malut_berita'
    allowed_domains = [ 'beritamalut.co' ]
    start_urls = [
        'http://beritamalut.co/page/1',
    ]
   

    def parse(self, response):
        """ Retrieve article list """
        self.logger.info('>> PROCESSING in parse %s\n', response.url)
        for link in response.xpath('//div[@class="jeg_main_content col-sm-8"]//a[ancestor::h3]/@href').getall():
            self.logger.info('>> link in indeks page %s\n', link)
            yield scrapy.Request(link, callback=self.parse_article_page)

        self.cur_page = self.cur_page + 1
        if self.cur_page <= self.max_page :
            next_url = self.page_url + str(self.cur_page)
            self.logger.info(">>> NEXT URL: %s ", next_url)
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_article_page(self, response):
        self.logger.info('>> PROCESSING in parse_detail %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('.//h1[@class="jeg_post_title"]//text()').get() 
        item['date'] = response.xpath('.//div[@class="jeg_meta_date"]/a/text()').get()
        content = response.xpath('//div[@class="content-inner "]//p//text()').getall()
        item['content']  = "".join(content)
        yield item
