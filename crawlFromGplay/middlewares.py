# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse
import time


class SeleniumDownloadMiddleware(object):
    """使用Selenium模拟启动浏览器
        点击链接爬取页面动态加载信息
        发送POST请求更加快速"""
    def __init__(self):
        self.driver = webdriver.Chrome()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(0.5)
        try:
            while True:
                ShowMore = self.driver.find_element_by_xpath('//a[@jsname="Hly47e"]')
                ShowMore.click()
                if not ShowMore:
                    break
        except:
            pass
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=source, encoding='utf-8', request=request)
        return response
