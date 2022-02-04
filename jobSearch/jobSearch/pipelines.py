# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql
from twisted.enterprise import adbapi

class JobsearchPipeline:
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
            charset='utf8',
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
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常

    def do_insert(self, cursor, item):
        cursor.execute("""select * from amazon where origin_id = %s""", item['origin_id'])
        # 是否有重复数据
        repetition = cursor.fetchone()

        # 重复
        if repetition:
            pass
        else:
            # 对数据库进行插入操作，并不需要commit，twisted会自动commit
            insert_sql = """insert into amazon(basic_qualifications, business_category,city,
            company_name,country_code,description,job_category,job_family,job_schedule_type,
            normalized_location,posted_date,preferred_qualifications,title,updated_time,
            url_next_step,origin_id)
            value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_sql,
                                (
                                    item['basic_qualifications'],
                                    item['business_category'],
                                    item['city'],
                                    item['company_name'],
                                    item['country_code'],
                                    item['description'],
                                    item['job_category'],
                                    item['job_family'],
                                    item['job_schedule_type'],
                                    item['normalized_location'],
                                    item['posted_date'],
                                    item['preferred_qualifications'],
                                    item['title'],
                                    item['updated_time'],
                                    item['url_next_step'],
                                    item['origin_id'])
                                )

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)
