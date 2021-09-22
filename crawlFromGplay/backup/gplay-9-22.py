import scrapy
from crawlFromGplay.items import CrawlfromgplayItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import pandas as pd


class GplaySpider(scrapy.Spider):
    """爬取页面静态信息"""
    """9-22"""
    name = 'gplay'
    allowed_domains = ["play.google.com"]

    # 从Excel中读包名
    # data = pd.read_csv('PHL_app_scrape.csv')
    data = pd.read_csv('pageage_name_PH.csv')
    # data = pd.read_excel('appInfo_test.xlsx')
    result = data.values.tolist()
    urls = []
    for s in result:
        urls.append('https://play.google.com/store/apps/details?id=' + s[0])
    start_urls = urls

    # 爬取规则
    rules = (
        Rule(LinkExtractor(allow=('/store/apps',), deny=('/store/apps/details',)), follow=True),
        Rule(LinkExtractor(allow=("/store/apps/details",)), follow=True, callback='parse_link'),
    )

    # 循环爬取
    def parse_start_url(self, response):
        return scrapy.Request(url=response.url, callback=self.parse)

    def parse(self, response):
        titles = response.xpath('/html')
        for title in titles:
            item = CrawlfromgplayItem()
            item['title'] = title.xpath('//h1[@class="AHFaub"]/span/text()').extract_first()
            item['appId'] = title.xpath('/html/head/meta[19]/@content').extract_first()
            item['description'] = title.xpath('//div[@jsname="sngebd"]/text()').extract()
            item['summary'] = title.xpath('//meta[@name="description"]/@content').extract_first()
            item['url'] = title.xpath('/html/head/link[4]/@href').extract_first()
            item['installs'] = title.xpath('//div[contains(text(),"Installs")]/following-sibling::span/div/span/text()').extract_first()
            item['score'] = title.xpath('//div[@class="BHMmbe"]/text()').extract_first()
            item['reviews'] = title.xpath('//span[@class="EymY4b"]/span[2]/text()').extract_first()
            item['price'] = title.xpath('//span[@class="oocvOe"]/button/@aria-label').extract_first()
            item['size'] = title.xpath('//div[contains(text(),"Size")]/following-sibling::span/div/span/text()').extract_first()
            item['androidVersion'] = title.xpath('//div[contains(text(),"Requires Android")]/following-sibling::span/div/span/text()').extract_first()
            item['developer'] = title.xpath('//a[@class="hrTbp R8zArc"]/text()').extract_first()
            item['genre'] = title.xpath('//a[@itemprop="genre"]/text()').extract_first()
            item['contentRating'] = title.xpath('//div[contains(text(),"Content Rating")]/following-sibling::span/div/span/div/text()').extract_first()




            item['Icon'] = title.xpath('//div[@class="xSyT2c"]/img/@src').extract_first()
            item['Rating'] = title.xpath('//div[@class="pf5lIe"]/div/@aria-label').extract_first()
            item['Update'] = title.xpath('//div[contains(text(),"Updated")]/following-sibling::span/div/span/text()').extract_first()
            item['Developer_website'] = title.xpath('//div[contains(text(),"Developer")]/following-sibling::span/div/span/div/a/@href').extract()[0]
            item['Developer_email'] = title.xpath('//div[contains(text(),"Developer")]/following-sibling::span/div/span/div/a[@class="hrTbp euBY6b"]/text()').extract_first()
            item['Developer_address'] = title.xpath('//div[contains(text(),"Developer")]/following-sibling::span/div/span/div/text()').extract_first()
            item['Similar'] = title.xpath('//div[@class="WsMG1c nnK0zc"]/text()').extract()
            item['Version'] = title.xpath('//div[contains(text(),"Version")]/following-sibling::span/div/span/text()').extract_first()
            yield item



