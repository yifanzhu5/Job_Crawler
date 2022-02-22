

import scrapy
import requests
import json
import csv
from ..items import AmazonItem
import datetime
import time

class AmazonJobsSpider(scrapy.Spider):
    '''
    f = open('amazon.csv', mode='a', encoding='utf-8', newline='')
    csv_writer = csv.DictWriter(f, fieldnames=["basic_qualifications",
                                               "team",
                                               "city",
                                               "company",
                                               "locations",
                                               "description",
                                               "job_category",
                                               "job_family",
                                               "job_schedule_type",
                                               "publish_time",
                                               "preferred_qualifications",
                                               "title",
                                               "update_time",
                                               "apply_url"
                                               "from_url"
                                               "origin_id"
                                               ])
    csv_writer.writeheader()
    '''

    name = 'amazon_jobs'
    start_urls = ['https://www.amazon.jobs/en/search.json?'\
                  'category%5B%5D=software-development&' \
                  'normalized_country_code%5B%5D=CAN&' \
                  'radius=100000km&' \
                  'facets%5B%5D=normalized_country_code&' \
                  'facets%5B%5D=normalized_state_name&' \
                  'facets%5B%5D=normalized_city_name&' \
                  'facets%5B%5D=location&' \
                  'facets%5B%5D=business_category&' \
                  'facets%5B%5D=category&' \
                  'facets%5B%5D=schedule_type_id&' \
                  'facets%5B%5D=employee_class&' \
                  'facets%5B%5D=normalized_location&' \
                  'facets%5B%5D=job_function_id&' \
                  'facets%5B%5D=is_manager&' \
                  'facets%5B%5D=is_intern&' \
                  'offset=0&' \
                  'result_limit=10&sort=relevant&latitude=45.42179&longitude=-75.69116&loc_group_id=&loc_query=Canada&base_query=&city=&country=CAN&region=&county=&query_options=&'

]

    page = 1
    total_page = 0
    page_url = 'https://www.amazon.jobs/en/search.json?'\
                  'category%5B%5D={}&' \
                  'normalized_country_code%5B%5D=CAN&' \
                  'radius=100000km&' \
                  'facets%5B%5D=normalized_country_code&' \
                  'facets%5B%5D=normalized_state_name&' \
                  'facets%5B%5D=normalized_city_name&' \
                  'facets%5B%5D=location&' \
                  'facets%5B%5D=business_category&' \
                  'facets%5B%5D=category&' \
                  'facets%5B%5D=schedule_type_id&' \
                  'facets%5B%5D=employee_class&' \
                  'facets%5B%5D=normalized_location&' \
                  'facets%5B%5D=job_function_id&' \
                  'facets%5B%5D=is_manager&' \
                  'facets%5B%5D=is_intern&' \
                  'offset={}&' \
                  'result_limit=10&sort=relevant&latitude=45.42179&longitude=-75.69116&loc_group_id=&loc_query=Canada&base_query=&city=&country=CAN&region=&county=&query_options=&'


    def start_requests(self):
        headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        }

        reqUrl = self.page_url.format('software-development', (self.page - 1) * 10)
        html_data = requests.get(url=reqUrl, headers=headers).text
        json_data = json.loads(html_data)
        self.total_page = (json_data["hits"] / 10 if json_data["hits"] % 10 == 0
                           else (json_data["hits"] / 10) + 1)

        while self.page <= self.total_page:
            reqUrl = self.page_url.format('software-development', (self.page - 1) * 10)
            yield scrapy.Request(reqUrl, callback=self.parse)
            self.page += 1

    def parse(self, response):

        print('crawling amazon')
        html_data = response.text
        json_data = json.loads(html_data)
        jobs = json_data["jobs"]


        for job in jobs:
            posted_time=job["posted_date"]+" 00:00:00"
            timeArray = time.strptime(posted_time, "%B %d, %Y %H:%M:%S")
            timestamp = int(time.mktime(timeArray))

            basic_qualifications = job["basic_qualifications"]
            business_category = job["business_category"]
            city = job["city"]
            company_name = job["company_name"]
            location = job["city"]
            description = job["description"]
            job_category = job["job_category"]
            job_family = job["job_family"]
            job_schedule_type = job["job_schedule_type"]
            publish_time = timestamp
            preferred_qualifications = job["preferred_qualifications"]
            title = job["title"]
            updated_time = job["updated_time"]
            url_next_step = job["url_next_step"]
            origin_id = job["id_icims"]
            '''
            dict = {
                "basic_qualifications": basic_qualifications,
                "business_category": business_category,
                "city": city,
                "company": company_name,
                "locations": location,
                "description": description,
                "job_category": job_category,
                "job_family": job_family,
                "job_schedule_type": job_schedule_type,
                "publish_time": publish_time,
                "preferred_qualifications": preferred_qualifications,
                "title": title,
                "update_time": updated_time,
                "apply_url": url_next_step,
                "from_url" : 'https://jobs-us-east.amazon.com/en/jobs/' + origin_id,
                "origin_id" : origin_id
            }
            self.csv_writer.writerow(dict)
            '''
            item = AmazonItem()
            item['basic_qualifications'] = basic_qualifications
            item['team'] = business_category
            item['city'] = city
            item['company'] = 'Amazon'
            item['locations'] = location
            item['description'] = description
            item['job_category'] = job_category
            item['job_family'] = job_family
            item['job_schedule_type'] = job_schedule_type
            item['publish_time'] = publish_time
            item['preferred_qualifications'] = preferred_qualifications
            item['title'] = title
            item['update_time'] = updated_time
            item['apply_url'] = url_next_step
            item['origin_id'] = origin_id
            item['from_url'] = 'https://jobs-us-east.amazon.com/en/jobs/' + origin_id
            item['has_remote'] = False
            item['subcompany'] = company_name

            yield item



