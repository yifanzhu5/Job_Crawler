#### Description
This is a demo to crawl sde jobs in Canada from Amazon job website using scrapy in an asynchronized way and insert the data into the mySQL database directly asynchronously.

#### Environment
pip install scrapy
pip install pymysql

#### How to use
1. build crawler python script under spiders directory: enter spider directory, use command:
scrapy genspider spiderName www.xxx.com
2. modify items.py, replace items in the JobsearchItem class with your own data entry names
3. modify pipelines.py, replace insert_sql and cursor.execute() with your own database table name and the specific item entries.
4. modify settings.py, replace MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWD with your own mySQL settings.
5. use command: scrapy crawl spiderName to start crawling. 
