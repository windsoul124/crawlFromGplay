# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from twisted.enterprise import adbapi


# 异步更新操作
class CrawlfromgplayPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )

        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常

    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql = """
        insert into vn_app_info(app_name, package_name, description, summary, url, 
        installs, min_installs, score, ratings, price, currency, 
        size, android_version, android_version_text, developer, 
        privacy_policy, genre, genre_id, content_rating, contains_ads, 
        version, released) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(insert_sql, (item['title'],  item['appId'], item['description'],
                                    item['summary'],  item['url'], item['installs'],
                                    item['minInstalls'], item['score'], item['ratings'],
                                    item['price'], item['currency'], item['size'],
                                    item['androidVersion'], item['androidVersionText'], item['developer'],
                                    item['privacyPolicy'], item['genre'], item['genreId'],
                                    item['contentRating'], item['containsAds'], item['version'],
                                    item['released']
                                     ))

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)
