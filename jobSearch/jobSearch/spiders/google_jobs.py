import scrapy
import requests
import json
from ..items import GoogleItem


class GoogleJobsSpider(scrapy.Spider):
    name = 'google_jobs'
    allowed_domains = ['careers.google.com/jobs/results']
    start_urls = ['http://careers.google.com/jobs/results/']

    page = 1
    total_page = 0
    page_url = "https://careers.google.com/api/v3/search/?page={}&q="

    def start_requests(self):
        headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        }

        reqUrl = self.page_url.format((self.page - 1) * 10)
        html_data = requests.get(url=reqUrl, headers=headers).text
        json_data = json.loads(html_data)
        self.total_page = (json_data["count"] / 20 if json_data["count"] % 20 == 0
                           else (json_data["count"] / 20) + 1)
        print("total page: ", end="")
        print(self.total_page)

        while self.page <= self.total_page:
            reqUrl = self.page_url.format((self.page - 1) * 10)
            yield scrapy.Request(reqUrl, callback=self.parse)
            self.page += 1

    def parse(self, response):
        print('crawling google')
        html_data = response.text
        json_data = json.loads(html_data)
        jobs = json_data["jobs"]

        for job in jobs:
            id = job["id"]
            title = job["title"]
            # categories = job["categories"]
            apply_url = job["apply_url"]
            # responsibilities = job["responsibilities"]
            # qualifications = job["qualifications"]
            company_name = job["company_name"]
            locations = job["locations"]
            description = job["description"]
            # education_levels = job["education_levels"]
            publish_date = job["publish_date"]
            # locations_count = job["locations_count"]
            # additional_instructions = job["additional_instructions"]
            # summary = job["summary"]
            # building_pins = job["building_pins"]
            # has_remote = job["has_remote"]


        item = GoogleItem()
        item['title'] = title
        item['publish_time'] = publish_date
        item['locations'] = locations
        item['description'] = description
        item['company'] = company_name
        item['apply_url'] = apply_url
        item['from_url'] = "https://careers.google.com/jobs/results/" + "-" + id + "-" + title.replace(", ", "-")

        yield item
