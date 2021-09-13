import scrapy
from crawlFromGplay.items import CrawlfromgplayItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import pandas as pd
from urllib.parse import urlparse
class GplaySpider(scrapy.Spider):
    name = 'gplay'
    allowed_domains = ["play.google.com"]
    data = pd.read_excel('appInfo.xlsx')
    result = data.values.tolist()
    urls = []
    for s in result:

        urls.append('https://play.google.com/store/apps/details?id='+ s[2])
    start_urls = urls

    rules = (
        Rule(LinkExtractor(allow=('/store/apps',), deny=('/store/apps/details',)), follow=True),
        Rule(LinkExtractor(allow=("/store/apps/details",)), follow=True, callback='parse_link'),
    )
    def parse_start_url(self, response):
        return scrapy.Request(url=response.url, callback=self.parse)

    def parse(self, response):
        items = 0
        titles = response.xpath('/html')
        for title in titles:
            item = CrawlfromgplayItem()
            item['Link'] = title.xpath('/html/head/link[4]/@href').extract_first()

            item['Icon'] = title.xpath('//div[@class="xSyT2c"]/img/@src').extract_first()
            item['Item_name'] = title.xpath('//h1[@class="AHFaub"]/span/text()').extract_first()
            item['Author'] = title.xpath('//a[@class="hrTbp R8zArc"]/text()').extract_first()
            item['Category'] = title.xpath('//a[@itemprop="genre"]/text()').extract_first()
            item['Rating'] = title.xpath('//div[@class="pf5lIe"]/div/@aria-label').extract_first()
            item['Detail'] = title.xpath('//div[@jsname="sngebd"]/text()').extract()
            item['Description'] = title.xpath('//meta[@name="description"]/@content').extract_first()
            item['Review_number'] = title.xpath('//span[@class="EymY4b"]/span[2]/text()').extract_first()
            item['Update'] = title.xpath('//div[contains(text(),"Updated")]/following-sibling::span/div/span/text()').extract_first()
            item['Size'] = title.xpath('//div[contains(text(),"Size")]/following-sibling::span/div/span/text()').extract_first()
            item['Installs'] = title.xpath('//div[contains(text(),"Installs")]/following-sibling::span/div/span/text()').extract_first()
            item['Version'] = title.xpath('//div[contains(text(),"Version")]/following-sibling::span/div/span/text()').extract_first()
            item['Compatibility'] = title.xpath('//div[contains(text(),"Requires Android")]/following-sibling::span/div/span/text()').extract_first()
            item['Content_rating'] = title.xpath('//div[contains(text(),"Content Rating")]/following-sibling::span/div/span/div/text()').extract_first()
            # item['Authority'] = response.xpath('//li[@class="BCMWSd"]').extract()
            item['Developer_website'] = title.xpath('//div[contains(text(),"Developer")]/following-sibling::span/div/span/div/a/@href').extract()[0]
            # item['Developer_email'] = title.xpath('//div[contains(text(),"Developer")]/following-sibling::span/div/span/div/a/@href').extract()[1]
            # item['Developer_address'] = title.xpath('//div[contains(text(),"Developer")]/following-sibling::span/div/span/div/a/@href').extract()[2]
            item['Package'] = title.xpath('/html/head/meta[19]/@content').extract_first()
            yield item



