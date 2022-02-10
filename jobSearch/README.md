#### Description
This is a demo to crawl sde jobs in Canada from a group of job websites using scrapy in an asynchronized way and insert the data into the mySQL database directly asynchronously.

#### Environment
pip install scrapy

pip install pymysql

#### How to use
1. Prepare mySQL database

Create one table(or tables for all websites) in your mySQL database with 5 mandatory columns : **publish_time, description, company, apply_url, from_url**(make sure the datatype is big enough for all these contents).

And some other columns according to the website information(already used by Amazon or Shopify data) : **basic_qualifications, team, city, job_category, job_family, job_schedule_type, preferred_qualifications, title, update_time, new_grad, origin_id**.

Or you can create new columns for certain websites.
2. Generate spider file

Enter spider directory under jobSearch dir, use command:
"scrapy genspider spiderName www.xxx.com".
3. Add spider file to start file

Modify crawler.py under jobSearch dir, add "process.crawl('spiderName')" before "process.start()".
4. Define items

(1) Modify items.py, add newItem class and enter items with your own data entry names. 

(2) Go to your spider file, add "from ..items import newItem"
5. Define piplines

(1) Modify MultiPipeline class in pipelines.py, add new elif process in "process_item" function

(2) Add new_insert function, replace insert_sql and cursor.execute() with your own database table name and the specific item entries.
6. Define database settings

Modify settings.py, replace MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWD with your own mySQL settings.
7. Start Running

**If you just want to crawl one specific website:**
use command: "scrapy crawl spiderName".

**If you want to crawl all websites simultaneously:**
use command: "python crawler.py".