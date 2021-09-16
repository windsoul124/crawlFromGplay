import copy

import scrapy
from crawlFromGplay.items import CrawlfromgplayItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import pandas as pd
from urllib.parse import urlparse


class GplaySpider(scrapy.Spider):
    """正常爬取每页数据
       通过Excel读取"""
    name = 'gallplay'
    allowed_domains = ["play.google.com"]
    # data = pd.read_csv('PHL_app_scrape.csv')
    # data = pd.read_csv('pageage_name_PH.csv')
    data = pd.read_excel('appInfo_test.xlsx')
    result = data.values.tolist()
    urls = []
    package = []
    for s in result:
        urls.append('https://play.google.com/store/apps/details?id=' + s[2])
        package.append(s[2])
    start_urls = urls

    rules = (
        Rule(LinkExtractor(allow=('/store/apps',), deny=('/store/apps/details',)), follow=True),
        Rule(LinkExtractor(allow=("/store/apps/details",)), follow=True, callback='parse_link'),
    )

    # def parse_start_url(self, response):
    #     return scrapy.Request(url=response.url, callback=self.parse)

    def parse(self, response):
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
            yield scrapy.Request(url=response.url, callback=self.parse_second, meta={'item': copy.deepcopy(item)})

    def parse_second(self, response):
        item = response.meta['item']
        print(item['Package'])
        headers = {
            'authority': 'play.google.com',
            'method': 'POST',
            'path': '/_/PlayStoreUi/data/batchexecute?rpcids=xdSrCf&f.sid=9134387918252213253&bl=boq_playuiserver_20210908.03_p0&hl=en-US&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=161734&rt=c',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'cookie': '_ga=GA1.3.2136857255.1631268520; OTZ=6149409_24_24__24_; _gid=GA1.3.2111573926.1631496501; NID=223=k1SGaaPoX_GfWEuYnHA5S2dHAMP95THwEbDKyrK-23X5LuMkSBhVoJZTgY2TFGY_LS6_QC8RExEtx0HPX9dVfdDsCKfg-24HI6R3XmpdMZ0O2KnX_JL9jDDde0VLyEwMeGcrFJhMrophY01FwizE14RaRDLJh0HMToP5E85Hdx6GDeZSqMKIcAojqL6U03CI4ns; 1P_JAR=2021-09-14-08; _gat_UA199959031=1',
            'origin': 'https://play.google.com',
            'referer': 'https://play.google.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        }
        url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute?hl=en&gl=us'
        data = {
            'f.req': '[[["xdSrCf","[[null,[\\"{0}{1}"'.format(item['Package'], '\\",7],[]]]",null,"1"]]]'),
        }
        print(data)
        item['Authority'] = response.text
        # yield scrapy.FormRequest(url, headers=headers, formdata=data, callback=self.parse_second)


