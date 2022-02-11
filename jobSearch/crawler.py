from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 添加爬虫名
process.crawl('amazon_jobs')
process.crawl('google_jobs')
process.crawl('shopify_jobs')
process.crawl('glassdoor_jobs')

process.start()
