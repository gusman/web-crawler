import scrapy
import string

class ItemNews(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
#    url = scrapy.Field()

class PostKotaSpider(scrapy.Spider):
    max_page = 7605
    cur_page = 1
    page_url = 'https://poskota.id/index-berita/page/'

    name = "jakarta_poskota"
    allowed_domains = [ 'poskota.id' ]
    start_urls = [
        'https://poskota.id/index-berita/page/1',
        #'https://poskota.id/2020/3/10/bertemu-komisi-viii-dpr-dubes-arab-saudi-kami-batasi-umrah-warga-lokal',
    ]
    
    def parse(self, response):
        """ Retrieve article list """
        self.logger.info('>> PROCESSING in parse %s\n', response.url)
        for link in response.xpath('//div[@class="content-artikel-list-box"]//a/@href').getall():
            self.logger.info('>> link in indekx page %s\n', link)
            yield scrapy.Request(link, callback=self.parse_article_page)

        self.cur_page = self.cur_page + 1
        if self.cur_page <= self.max_page :
            next_url = self.page_url + str(self.cur_page)
            self.logger.info(">>> NEXT URL: %s ", next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_article_page(self, response):
        self.logger.info('>> PROCESSING in parse_article_page %s\n', response.url)
        item = ItemNews()
        item['title'] = response.xpath('//h1[@class="title"]/text()').get()
        item['date'] = response.xpath('//div[@class="date"]/text()').get()
        content = response.xpath('//div[@class="text-box"]//text()').getall()
        clean_content = [ s.rstrip() for s in content ]
        item['content']  = "".join(clean_content)
        #item['url']  = response.url
        yield item
 
