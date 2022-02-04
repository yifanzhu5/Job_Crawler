# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsearchItem(scrapy.Item):
    # define the fields for your item here like:
    basic_qualifications = scrapy.Field()
    business_category = scrapy.Field()
    city = scrapy.Field()
    company_name = scrapy.Field()
    country_code = scrapy.Field()
    description = scrapy.Field()
    job_category = scrapy.Field()
    job_family = scrapy.Field()
    job_schedule_type = scrapy.Field()
    normalized_location = scrapy.Field()
    posted_date = scrapy.Field()
    preferred_qualifications = scrapy.Field()
    title = scrapy.Field()
    updated_time = scrapy.Field()
    url_next_step = scrapy.Field()
    origin_id = scrapy.Field()

