# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql
from twisted.enterprise import adbapi


class MultiPipeline:
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
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=3306,
            charset='utf8mb4',
            use_unicode=True,
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
        if spider.name == 'amazon_jobs':
            query = self.dbpool.runInteraction(self.amazon_insert, item)  # 指定操作方法和操作数据
            # 添加异常处理
            query.addCallback(self.handle_error)
        elif spider.name == 'shopify_jobs':
            query = self.dbpool.runInteraction(self.shopify_insert, item)  # 指定操作方法和操作数据
            # 添加异常处理
            query.addCallback(self.handle_error)
        # add your own elif process

    def amazon_insert(self, cursor, item):
        cursor.execute("""select * from jobs where from_url = %s""", item['from_url'])
        # 是否有重复数据
        repetition = cursor.fetchone()

        # 重复
        if repetition:
            pass
        else:
            # 对数据库进行插入操作，并不需要commit，twisted会自动commit
            # 根据表名和列名修改
            insert_sql = """insert into jobs(basic_qualifications,team,city,
            company,locations,description,job_category,job_family,job_schedule_type,
            publish_time,preferred_qualifications,title,update_time,
            apply_url,from_url)
            value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_sql,
                           (
                               item['basic_qualifications'],
                               item['team'],
                               item['city'],
                               item['company'],
                               item['locations'],
                               item['description'],
                               item['job_category'],
                               item['job_family'],
                               item['job_schedule_type'],
                               item['publish_time'],
                               item['preferred_qualifications'],
                               item['title'],
                               item['update_time'],
                               item['apply_url'],
                               item['from_url'])
                           )

    def shopify_insert(self, cursor, item):
        cursor.execute("""select * from jobs where from_url = %s""", item['from_url'])
        # 是否有重复数据
        repetition = cursor.fetchone()

        # 重复
        if repetition:
            pass
        else:
            # 对数据库进行插入操作，并不需要commit，twisted会自动commit
            insert_sql = """insert into jobs(title,company,locations,team,apply_url,new_grad,description,from_url,publish_time)
            value (%s, %s, %s, %s, %s, %s, %s, %s,%s)"""
            cursor.execute(insert_sql,
                           (
                               item['title'],
                               item['company'],
                               item['locations'],
                               item['team'],
                               item['apply_url'],
                               item['new_grad'],
                               item['description'],
                               item['from_url'],
                               item["publish_time"]
                           )
                           )

    # add your own insert function

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)
