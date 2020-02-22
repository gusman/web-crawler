import scrapy

class SinggalangSpider(scrapy.Spider):
    stop_flag = False
    name = "sumbar_singgalang"
    start_urls = [
        'https://hariansinggalang.co.id/',
    ]
    
    def parse(self, response):
        """ Retrieve article list """
        for article in response.xpath('//div[@class="item-article"]'):
            links_text = article.xpath('.//a/text()').get()
            links = article.xpath('.//a/@href').get()
            time = article.xpath('.//time/@datetime').get()
           
            if time.startswith("2018"):
                self.stop_flag = True

            yield scrapy.Request(links, callback=self.parse_article_page)

        if (False == self.stop_flag):
            next_url = response.xpath('//a[@class="next page-numbers"]/@href').get();
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_article_page(self, response):
        title = response.xpath('//h1[@itemprop="headline"]/text()').get()
        time  = response.xpath('//time/@datetime').get()
        content = response.xpath('//div[@class="entry-content entry-content-single"]/p/text()').getall()
        return {
            'title' : title,
            'time'  : time,
            'content': "".join(content),
        }

