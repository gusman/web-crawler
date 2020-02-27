import scrapy
from time import sleep
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains

class DewanPersSpider(scrapy.Spider):
    name = "dewan_pers"
    start_urls = [
        'https://dewanpers.or.id/data/perusahaanpers',
    ]
    list_links = []
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse_initial, headers=self.headers)

    def parse_initial(self, response):
        driver = response.request.meta['driver']
        
        el_select = driver.find_element_by_name("provinsi")
        Select(el_select).select_by_visible_text("Sumatera Barat")
        sleep(2)

        el_select = driver.find_element_by_name("status")
        Select(el_select).select_by_visible_text("Terverifikasi Administrasi & Faktual")
        sleep(2)

        el_filter = driver.find_element_by_xpath('//button[@id="btn-filter"]')
        ActionChains(driver).move_to_element(el_filter).click().perform()
        sleep(2)
        
        el_select = driver.find_element_by_name("data1_length")
        Select(el_select).select_by_visible_text("10")
        print("\n\n ------------ SELECT ACTION ----------------")
        sleep(5)

        while (1):
            rows = driver.find_elements_by_xpath("//tr[@role='row']")
            if 1 != self.parse_rows(driver, rows, 10):
                break;
    
        print("LEN: ", len (self.list_links))
        print(self.list_links)

    def parse_rows(self, driver, rows, n_row):
        if 1 < len(rows):
            for row in rows:
                data = row.find_elements_by_xpath('.//td')
                print ([ d.text for d in data ])
                cols = row.find_elements_by_xpath('.//a')
                self.list_links.extend([ col.text for col in cols ])
            
            if 0 != (len(self.list_links) % n_row):
                print(">> Ends loop no next page")
                return 0
            
            try:
                el_next = driver.find_element_by_link_text("Next")
                ActionChains(driver).move_to_element(el_next).click().perform()
                sleep(5)
            except Exception as e: 
                print('>> EXCEPTION: '+ str(e))
                return 0
            return 1
        else:
            return 0

    def parse(self, response):
        print("PARSING....")
        for row in response.selector.xpath('//*'):
            print(row.getall())



#        for row in response.xpath('//tr[@role="row"]'):
#            lst_media  = row.xpath('.//td/text()').getall()
#            link_media = row.xpath('.//a/text()').get()
#            lst_media.append(link_media)
#            print (lst_media)
##
