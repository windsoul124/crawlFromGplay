import json

import scrapy
import pandas as pd
import re
import urllib.request
from crawlFromGplay.element import *
class PostdemoSpider(scrapy.Spider):
    name = 'post'
    start_urls = [
            'https://play.google.com/_/PlayStoreUi/data/batchexecute?hl=en&gl=us']
    allowed_domains = []
    url = []
    data = pd.read_excel('appInfo.xlsx')
    result = data.values.tolist()
    # for s in result:
    #     url.append('[[["xdSrCf","[[null,[\\"{0}{1}"'.format(s[2], '\\",7],[]]]",null,"1"]]]')),
    #     # '[[["xdSrCf", "[[null,[\"com.google.android.youtube",7],[]]]", null, "1"]]]',
    # print(url)

    def start_requests(self):
        requests = []

        """循环"""
        # for i in range(len(self.url)):
        #     data = {
        #     # 'f.req': self.url[i],
        #     'f.req': '[[["xdSrCf","[[null,[\"com.google.android.youtube\",7],[]]]",null,"1"]]]',
        #     }
        #     print(data)
        #     for url in self.start_urls:
        #         yield scrapy.FormRequest(url, headers={"content-type": "application/x-www-form-urlencoded"}, formdata=data, callback=self.parse)
        data = {
            'f.req': '[[["xdSrCf","[[null,[\\"com.google.android.youtube\\",7],[]]]",null,"1"]]]'
        }
        headers={
                'authority': 'play.google.com',
                'method': 'POST',
                'path': '/_/PlayStoreUi/data/batchexecute?rpcids=xdSrCf&f.sid=9134387918252213253&bl=boq_playuiserver_20210908.03_p0&hl=en-US&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=161734&rt=c',
                'scheme': 'https',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9,zh;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
                # 'content-length': '139',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'cookie': '_ga=GA1.3.2136857255.1631268520; OTZ=6149409_24_24__24_; _gid=GA1.3.2111573926.1631496501; NID=223=k1SGaaPoX_GfWEuYnHA5S2dHAMP95THwEbDKyrK-23X5LuMkSBhVoJZTgY2TFGY_LS6_QC8RExEtx0HPX9dVfdDsCKfg-24HI6R3XmpdMZ0O2KnX_JL9jDDde0VLyEwMeGcrFJhMrophY01FwizE14RaRDLJh0HMToP5E85Hdx6GDeZSqMKIcAojqL6U03CI4ns; 1P_JAR=2021-09-14-08; _gat_UA199959031=1',
                'origin': 'https://play.google.com',
                'referer': 'https://play.google.com/',
                # 'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
                # 'sec-ch-ua-mobile': '?0',
                # 'sec-ch-ua-platform': '"Windows"',
                # 'sec-fetch-dest': 'empty',
                # 'sec-fetch-mode': 'cors',
                # 'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
                # 'x-client-data': 'CI62yQEIpbbJAQjBtskBCKmdygEIi9HKAQjKhcsBCO/yywEItPjLAQie+csBCK/6ywEIof7LAQi+/ssBCJ7/ywEIjYHMARjioMsB',
        }
        for url in self.start_urls:
            yield scrapy.FormRequest(url, headers=headers, formdata=data, callback=self.parse)

        #     request = scrapy.FormRequest(self.start_urls[0], headers={"content-type": "application/x-www-form-urlencoded"}, formdata=data, callback=self.parse)
        #     requests.append(request)
        # return requests
    # 该方法其实是父类中的一个方法：该方法可以对start_urls列表中的元素进行get请求的发送
    # 发起post：
    # 1.将Request方法中method参数赋值成post
    # 2.FormRequest()可以发起post请求（推荐）

    def parse(self, response):
        # response._DEFAULT_ENCODING = 'UTF-8'
        dom = str(response.text)
        PERMISSIONS = re.compile("\\)]}'\n\n([\s\S]+)")
        matches = json.loads(PERMISSIONS.findall(dom)[0])
        print(matches)
        # print(matches)
        container = json.loads(matches[0][2])
        # print(container)
        result = []
        # for permission_items in container:
        #     if isinstance(permission_items, list):
        #         print(permission_items)
        #         if len(permission_items[0]) == 2:
        #             permission_items = [["Uncategorized", None, permission_items, None]]
        #         for permission in permission_items:
        #             print(permission)
                    # result[
                    #     ElementSpecs.Permission_Type.extract_content(permission)
                    # ] = ElementSpecs.Permission_List.extract_content(permission)
                    # print(result)
        # print(container)
