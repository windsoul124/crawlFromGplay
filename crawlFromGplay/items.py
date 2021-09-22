# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class CrawlfromgplayItem(scrapy.Item):
    # apptitle（varchar）
    title = scrapy.Field()
    # app包名（varchar）
    appId = scrapy.Field()
    # app描述（varchar）
    description = scrapy.Field()
    # app短介绍（varchar）
    summary = scrapy.Field()
    # 链接（varchar）
    url = scrapy.Field()
    # 安装量（varchar）
    installs = scrapy.Field()
    # 最小安装量（varchar）
    minInstalls = scrapy.Field()
    # 得分(float)
    score = scrapy.Field()
    # 评级(int)
    ratings = scrapy.Field()
    # 价格(float)
    price = scrapy.Field()
    # 货币(varchar)
    currency = scrapy.Field()
    # app大小(varchar)
    size = scrapy.Field()
    # 安卓版本(varchar)
    androidVersion = scrapy.Field()
    # 安卓版本text(varchar)
    androidVersionText = scrapy.Field()
    # 开发者(varchar)
    developer = scrapy.Field()
    # 隐私政策(varchar)
    privacyPolicy = scrapy.Field()
    # app分类(varchar)
    genre = scrapy.Field()
    # app分类id(varchar)
    genreId = scrapy.Field()
    # 人群(varchar)
    contentRating = scrapy.Field()
    # 是否包含广告(varchar)
    containsAds = scrapy.Field()
    # APP版本
    version = scrapy.Field()
    # 更新时间
    released = scrapy.Field()
    # 权限
    permission = scrapy.Field()

    # 图标
    # Icon = scrapy.Field()
    # 开发者网站
    # Developer_website = scrapy.Field()
    # 开发者邮箱
    # Developer_email = scrapy.Field()
    # 开发者地址
    # Developer_address = scrapy.Field()
    # 相似
    # Similar = scrapy.Field()


