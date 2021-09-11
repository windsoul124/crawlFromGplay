# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse
import time
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(0.5)
        try:
            while True:
                ShowMore1 = self.driver.find_element_by_xpath('//a[@jsname="Hly47e"]')
                ShowMore1.click()
                if not ShowMore1:
                    break
        except:
            pass
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=source, encoding='utf-8', request=request)
        return response

