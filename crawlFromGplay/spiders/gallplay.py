import scrapy
from crawlFromGplay.items import CrawlfromgplayItem
from scrapy.spiders import Rule
from urllib.parse import urlparse
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
class LanguageLinkExtractor(LxmlLinkExtractor):
    # def __init__(self, allow=(), deny=(), allow_domains=(), deny_domains=(), restrict_xpaths=(),
    #              canonicalize=True,
    #              unique=True, process_value=None, deny_extensions=None, restrict_css=()):
    #     super(LxmlLinkExtractor, self).__init__(allow=allow, deny=deny,
    #         allow_domains=allow_domains, deny_domains=deny_domains,
    #         restrict_xpaths=restrict_xpaths, canonicalize=canonicalize,
    #         deny_extensions=deny_extensions, restrict_css=restrict_css)
    @staticmethod
    def addParams(url):
        if url.find('?') >= 0:
            return url+'&hl=en';
        else:
            return url +'?hl=en';


    def extract_links(self, response):
        links = LxmlLinkExtractor.extract_links(self, response);
        for x in links:
            x.url = LanguageLinkExtractor.addParams(x.url)
        # links = super(LxmlLinkExtractor, self).extract_links(response);
        return links;

class GplaySpider(scrapy.Spider):

    name = 'gallplay'
    allowed_domains = ["play.google.com"]

    start_urls =['http://play.google.com/',
        'https://play.google.com/store/apps/details?id=me.ele']

    rules = [
        Rule(LanguageLinkExtractor(allow=("/store/apps/details",)), callback='parse', follow=True),
    ]
    def parse(self, response):
        r = urlparse.urlparse(response.url);
        params = urlparse.parse_qs(r.query, True);
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
            item['Developer_email'] = title.xpath('//div[contains(text(),"Developer")]/following-sibling::span/div/span/div/a/@href').extract()[1]
            item['Developer_address'] = title.xpath('//div[contains(text(),"Developer")]/following-sibling::span/div/span/div/a/@href').extract()[2]
            yield item


