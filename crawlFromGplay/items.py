# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class CrawlfromgplayItem(scrapy.Item):
    # 链接
    Link = scrapy.Field()
    # 图标
    Icon = scrapy.Field()
    # 名字
    Item_name = scrapy.Field()
    # 作者
    Author = scrapy.Field()
    # 分类
    Category = scrapy.Field()
    # 评分
    Rating = scrapy.Field()
    # 简介
    Detail = scrapy.Field()
    # 介绍
    Description = scrapy.Field()
    # 人数
    Review_number = scrapy.Field()
    # 更新时间
    Update = scrapy.Field()
    # 大小
    Size = scrapy.Field()
    # 安装次数
    Installs = scrapy.Field()
    # 版本
    Version = scrapy.Field()
    # Andriod系统版本要求
    Compatibility = scrapy.Field()
    # 内容分级
    Content_rating = scrapy.Field()
    # 权限
    Authority = scrapy.Field()
    # 开发者网站
    Developer_website = scrapy.Field()
    # 开发者邮箱
    Developer_email = scrapy.Field()
    # 开发者地址
    Developer_address = scrapy.Field()
    # 包名
    Package = scrapy.Field()
    # 价钱（Install为免费，收费则显示价格）
    Price = scrapy.Field()
    # 分数
    Score = scrapy.Field()
    # 相似
    Similar = scrapy.Field()
    # 测试

