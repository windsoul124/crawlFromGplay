import scrapy
from crawlFromGplay.items import CrawlfromgplayItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import pandas as pd
import json
import re


class GplaySpider(scrapy.Spider):
    """爬取页面静态信息"""
    name = 'gplay'
    allowed_domains = ["play.google.com"]

    # 从Excel中读包名
    # data = pd.read_csv('PHL_app_scrape.csv')
    # data = pd.read_csv('pageage_name_VN.csv')
    data = pd.read_excel('appInfo_test.xlsx')
    result = data.values.tolist()
    urls = []
    for s in result:
        urls.append('https://play.google.com/store/apps/details?id=' + s[2])
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
        emoji_pattern = re.compile(
            u"(\ud83d[\ude00-\ude4f])|"  # emoticons
            u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
            u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
            u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
            u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
            "+", flags=re.UNICODE)
        titles = response.xpath('/html')
        for title in titles:
            item = CrawlfromgplayItem()
            item['title'] = title.xpath('//h1[@class="AHFaub"]/span/text()').extract_first()
            item['appId'] = title.xpath('/html/head/meta[19]/@content').extract_first()
            # item['description'] =  emoji_pattern.search(title.xpath('//div[@jsname="sngebd"]/text()').extract()).encode('unicode-escape')
            # item['description'] = title.xpath('//div[@jsname="sngebd"]/text()').extract()
            list = title.xpath('//div[@jsname="sngebd"]/text()').extract()
            s = ' '.join(list)
            item['description'] = s
            item['summary'] = title.xpath('//meta[@name="description"]/@content').extract_first()
            item['url'] = title.xpath('/html/head/link[4]/@href').extract_first()
            item['installs'] = title.xpath(
                '//div[contains(text(),"Installs")]/following-sibling::span/div/span/text()').extract_first()
            item['price'] = title.xpath('//span[@class="oocvOe"]/button/@aria-label').extract_first()
            item['size'] = title.xpath(
                '//div[contains(text(),"Size")]/following-sibling::span/div/span/text()').extract_first()
            item['androidVersionText'] = title.xpath(
                '//div[contains(text(),"Requires Android")]/following-sibling::span/div/span/text()').extract_first()
            item['androidVersion'] = title.xpath(
                '//div[contains(text(),"Requires Android")]/following-sibling::span/div/span/text()').extract_first().replace(
                ' and up', '')
            item['developer'] = title.xpath('//a[@class="hrTbp R8zArc"]/text()').extract_first()
            item['genre'] = title.xpath('//a[@itemprop="genre"]/text()').extract_first()
            item['contentRating'] = title.xpath(
                '//div[contains(text(),"Content Rating")]/following-sibling::span/div/span/div/text()').extract_first()
            item['minInstalls'] = title.xpath(
                '//div[contains(text(),"Installs")]/following-sibling::span/div/span/text()').extract_first().replace(
                ',', '').replace('+', '')
            item['released'] = title.xpath(
                '//div[contains(text(),"Updated")]/following-sibling::span/div/span/text()').extract_first()
            item['version'] = title.xpath(
                '//div[contains(text(),"Version")]/following-sibling::span/div/span/text()').extract_first()
            item['privacyPolicy'] = title.xpath(
                '//span[@class="htlgb"]/div/a[contains(text(), "Privacy Policy")]/@href').extract_first()
            dom = title.xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/script/text()').extract()
            match = json.loads(dom[0])
            contains_offer = match['offers']
            item['price'] = contains_offer[0]['price']
            item['currency'] = contains_offer[0]['priceCurrency']
            contains_aggregate = match['aggregateRating']
            item['score'] = contains_aggregate['ratingValue']
            item['ratings'] = contains_aggregate['ratingCount']
            item['genreId'] = match['applicationCategory']
            item['containsAds'] = title.xpath(
                '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/div[2]/text()').extract_first()
            yield item



