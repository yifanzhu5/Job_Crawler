# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GlassdoorItem(scrapy.Item):
    company = scrapy.Field()
    city = scrapy.Field()
    description = scrapy.Field()
    #job_category = scrapy.Field()
    #job_schedule_type = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    glassdoor_id = scrapy.Field()
    from_url = scrapy.Field()
    has_remote=scrapy.Field()





class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    basic_qualifications = scrapy.Field()
    team = scrapy.Field()
    city = scrapy.Field()
    company = scrapy.Field()
    locations = scrapy.Field()
    description = scrapy.Field()
    job_category = scrapy.Field()
    job_family = scrapy.Field()
    job_schedule_type = scrapy.Field()
    update_time = scrapy.Field()
    preferred_qualifications = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    apply_url = scrapy.Field()
    origin_id = scrapy.Field()
    from_url = scrapy.Field()
    has_remote = scrapy.Field()
    subcompany = scrapy.Field()

class GoogleItem(scrapy.Item):
    title = scrapy.Field()
    publish_time = scrapy.Field()
    locations = scrapy.Field()
    description = scrapy.Field()
    company = scrapy.Field()
    apply_url = scrapy.Field()
    from_url = scrapy.Field()

class ShopifyItem(scrapy.Item):
    team = scrapy.Field()
    publish_time = scrapy.Field()
    locations = scrapy.Field()
    company = scrapy.Field()
    description = scrapy.Field()
    title = scrapy.Field()
    from_url = scrapy.Field()
    apply_url = scrapy.Field()
    new_grad = scrapy.Field()
    has_remote = scrapy.Field()
    city = scrapy.Field()

# add your new item class
