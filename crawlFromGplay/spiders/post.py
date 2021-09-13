import scrapy


class PostdemoSpider(scrapy.Spider):
    name = 'post'
    start_urls = [
            'https://play.google.com/_/PlayStoreUi/data/batchexecute?rpcids=xdSrCf&f.sid=-3751894382704443719&bl=boq_playuiserver_20210908.03_p0&hl=en-US&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=164510&rt=c']
    allowed_domains = []

    def start_requests(self):
        data = {
            'f.req': '[[["xdSrCf","[[null,[\\"com.sc.scorecreator\\",7],[]]]",null,"1"]]]',
        }
        for url in self.start_urls:
            yield scrapy.FormRequest(url, headers={"content-type": "application/x-www-form-urlencoded"}, formdata=data, callback=self.parse)
    # 该方法其实是父类中的一个方法：该方法可以对start_urls列表中的元素进行get请求的发送
    # 发起post：
    # 1.将Request方法中method参数赋值成post
    # 2.FormRequest()可以发起post请求（推荐）

    def parse(self, response):
        print(response.xpath('.').extract())