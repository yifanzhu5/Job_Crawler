import scrapy
import requests
import json
import csv
from ..items import ShopifyItem
import datetime
import time
import re
from parsel import Selector
from bs4 import BeautifulSoup


class ShopifyJobsSpider(scrapy.Spider):
    name = 'shopify_jobs'
    url = 'https://www.shopify.com/careers/search?teams%5B%5D=data&teams%5B%5D=engineering&teams%5B%5D=interns&locations%5B%5D=Americas&locations%5B%5D=Canada&keywords=&sort=team_asc'
    timestamp = int(time.time())

    def start_requests(self):
        headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        }
        resp = requests.get(url=self.url, headers=headers)
        html_data = re.findall('"view job posting:" (.*?)</a>', resp.text)
        html_list = list(map(lambda sub: re.search('href="(.*?)"', sub).group(1), html_data))
        self.total_page = len(html_list)

        for i in html_list:
            # i[0] = i[0].replace('"', '').replace('href=', '')
            reqUrl = "https://www.shopify.com" + i
            request = scrapy.Request(reqUrl, callback=self.parse)
            request.cb_kwargs['reqUrl'] = reqUrl  # add more arguments for the callback
            yield request
        t2 = datetime.datetime.now()
        print("running time:" + str(t2 - self.t1))

    def parse(self, response, reqUrl):
        print('crawling shopify')
        html = response.text
        selector = Selector(html)
        location_data = selector.css(
            'table.job-info__table:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > a:nth-child(1)::text').get()
        title_data = selector.css('head > title:nth-child(7)::text').get().split(' | ')[0]
        if title_data.find('United States') == -1:  # not found
            team_data = selector.css(
                'table.job-info__table:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > a:nth-child(1)::text').get()



            Apply_now_data = selector.css('.button-light--indigo::attr(href)').get()

            JD_data = selector.css(
                '.job-posting__grid-content').get()  # save all job description (including About the role, Qualifications, How we hire) and their content as a css selector

            soup = BeautifulSoup(JD_data, 'html.parser')
            h2 = soup.find_all('h2')
            for h in h2:
                h.name = "h4"
            a = soup.find_all('a')
            a[len(a)-1].attrs['href']="https://www.shopify.com"+a[len(a)-1].attrs['href']
            JD_data = soup.prettify().replace("\n", "")

            if team_data == "Internships":
                new_graduate = True
            else:
                new_graduate = False
            if title_data.casefold().find("remote") != -1:
                remote_data = True
            else:
                remote_data = False

            item = ShopifyItem()
            item['title'] = title_data
            item['company'] = "Shopify"
            item['locations'] = location_data
            item['city'] = location_data.split(',')[0]
            item['team'] = team_data
            item['apply_url'] = Apply_now_data
            item['new_grad'] = new_graduate
            item['description'] = JD_data
            item['from_url'] = reqUrl
            item['publish_time'] = self.timestamp
            item["has_remote"] = remote_data

            yield item
