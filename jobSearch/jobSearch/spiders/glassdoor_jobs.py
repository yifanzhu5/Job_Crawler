import scrapy
import scrapy
import re
import json
from ..items import GlassdoorItem
from bs4 import BeautifulSoup as soup
import json
import requests
import urllib.request
from urllib.request import urlopen, Request
from urllib.parse import urlparse
import time

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def extract_listing(listing_soup):
    companyName, company_starRating, company_offeredRole, company_roleLocation = extract_listingBanner(listing_soup)
    listing_jobDesc = extract_listingDesc(listing_soup)

    return (companyName,company_offeredRole,company_roleLocation,listing_jobDesc)

def extract_listingBanner(listing_soup):
    listing_bannerGroup_valid = False

    try:
        listing_bannerGroup = listing_soup.find("div", class_="css-ur1szg e11nt52q0")
        listing_bannerGroup_valid = True
    except:
        print("[ERROR] Error occurred in function extract_listingBanner")
        companyName = "NA"
        company_starRating = "NA"
        company_offeredRole = "NA"
        company_roleLocation = "NA"

    if listing_bannerGroup_valid:
        try:
            company_starRating = listing_bannerGroup.find("span", class_="css-1pmc6te e11nt52q4").getText()
        except:
            company_starRating = "NA"
        if company_starRating != "NA":
            try:
                companyName = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").getText().replace(
                    company_starRating, '')
            except:
                companyName = "NA"
            # company_starRating.replace("★", "")
            company_starRating = company_starRating[:-1]
        else:
            try:
                companyName = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").getText()
            except:
                companyName = "NA"

        try:
            company_offeredRole = listing_bannerGroup.find("div", class_="css-17x2pwl e11nt52q6").getText()
        except:
            company_offeredRole = "NA"

        try:
            company_roleLocation = listing_bannerGroup.find("div", class_="css-1v5elnn e11nt52q2").getText()
        except:
            company_roleLocation = "NA"

    return companyName, company_starRating, company_offeredRole, company_roleLocation


# extracts desired data from listing description
def extract_listingDesc(listing_soup):
    listing_jobDesc_raw = None

    try:
        listing_jobDesc_raw = listing_soup.find("div", id="JobDescriptionContainer")
        if type(listing_jobDesc_raw) != type(None):
            listing_jobDesc=listing_jobDesc_raw
        else:
            JobDescriptionContainer_found = False
            listing_jobDesc = "NA"
    except Exception as e:
        #print("[ERROR] {} in extract_listingDesc".format(e))
        JobDescriptionContainer_found = False
        listing_jobDesc = "NA"
    return listing_jobDesc







def extract_listings(page_soup):

    listings_list = list()

    for a in page_soup.find_all('a', href=True):
        if "/partner/jobListing.htm?" in a['href']:
            # print("Found the URL:", a['href'])
            listings_list.append("www.glassdoor.com" + a['href'])

    listings_set = set(listings_list)
    jobCount = len(listings_set)

    try:
        assert jobCount != 0
    except Exception as e:
        print(e)
        print("[ERROR] Assumptions invalid")

    return listings_set, jobCount




def update_url(prev_url, page_index):
    if page_index == 1:
        prev_substring = ".htm"
        new_substring = "_IP" + str(page_index) + ".htm"
    else:
        prev_substring = "_IP" + str(page_index - 1) + ".htm"
        new_substring = "_IP" + str(page_index) + ".htm"

    new_url = prev_url.replace(prev_substring, new_substring)
    return new_url






def config():
    list=[]
    jobtype = ["jobType=fulltime", "jobType=parttime", "jobType=contract", "jobType=internship", "jobType=temporary"]
    posttime=[""]
    #posttime = ["fromAge=1", "fromAge=3", "fromAge=7", "fromAge=14", "fromAge=30"]
    senority = ["seniorityType=internship", "seniorityType=entrylevel", "seniorityType=midseniorlevel","seniorityType=director", "seniorityType=executive"]
    base=["https://www.glassdoor.ca/Job/canada-software-jobs-SRCH_IL.0,6_IN3_KO7,15.htm"]
    for itembase in base:
        for itemj in jobtype:
            for itemp in posttime:
                for items in senority:
                    if itemj == "":
                        if itemp == "":
                            if items == "":
                                url = itembase
                                list.append([url,"NA","NA","NA"])
                            else:
                                url = itembase + "?" + items
                                list.append([url,"NA","NA",items])
                        else:
                            if items == "":
                                url = itembase + "?" + itemp
                                list.append([url,"NA",itemp,"NA"])
                            else:
                                url = itembase + "?" + itemp + "&" + items
                                list.append([url,"NA",itemp,items])
                    else:
                        if itemp == "":
                            if items == "":
                                url = itembase + "?" + itemj
                                list.append([url, itemj, "NA", "NA"])
                            else:
                                url = itembase + "?" + itemj + "&" + items
                                list.append([url, itemj, "NA", items])
                        else:
                            if items == "":
                                url = itembase + "?" + itemj + "&" + itemp
                                list.append([url, itemj, itemp, "NA"])
                            else:
                                url = itembase + "?" + itemj + "&" + itemp + "&" + items
                                list.append([url, itemj , itemp, items])
    return list





class GlassdoorJobsSpider(scrapy.Spider):
    name = 'glassdoor_jobs'
    allowed_domains = ['glassdoor.com']



    def start_requests(self):
        qidian_headers = {
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 QQBrowser/9.3"}
        start_urls=config()

        for url in start_urls:
            yield scrapy.Request(url=url[0],meta={'url':url[0],'jobtype': url[1], 'posttime': url[2], 'senoritylevel':url[3]} ,callback=self.parse)


    def parse(self, response):
        para=[response.meta['jobtype'],response.meta['posttime'],response.meta['senoritylevel']]
        html_data = response.text
        page_soup = soup(html_data, "html.parser")

        # find max page and max job
        tmp_match_1 = [item for item in page_soup.find_all("p") if "data-test" in item.attrs][0]
        tmp_match_2 = [item for item in page_soup.find_all("div") if "data-test" in item.attrs][-2]
        maxJobs_raw = tmp_match_1.get_text()
        maxPages_raw = tmp_match_2.get_text()
        try:
            assert "Jobs" in maxJobs_raw
            assert "Page" in maxPages_raw
        except Exception as e:
            print(e)
            print("[ERROR] Assumptions invalid")

        maxJobs = re.sub(r"\D", "", maxJobs_raw)
        maxPages = re.sub(r"\D", "", maxPages_raw)[1:]



        list_nextstage=[]
        page_index = 1
        total_listingCount = 0
        prev_url = response.meta['url']
        list_nextstage.append(prev_url)
        while ((page_index <= int(maxPages)) and (total_listingCount <= int(maxJobs)) and (int(maxJobs) != 0)):
            new_url = update_url(prev_url, page_index)
            list_nextstage.append(new_url)
            page_index = page_index + 1
            prev_url = new_url

        qidian_headers = {
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 QQBrowser/9.3"}

        for url in list_nextstage:
            yield scrapy.Request(url=url,meta={'para':para,'url':url}, callback=self.parse_pages,dont_filter=True)

    def parse_pages(self,response):
        para_s=response.meta['para']
        html_data = response.text
        page_soup = soup(html_data, "html.parser")
        listings_set, jobCount = extract_listings(page_soup)
        time = page_soup.find_all("div", class_="d-flex align-items-end pl-std css-17n8uzw")


        i=0
        #qidian_headers = {"User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 QQBrowser/9.3"}
        for listing_url in listings_set:
            listing_url = 'https://' +listing_url
            string=str(time[i])
            x = string.index("job-age")
            y = string[x + 9:-6]
            i = i + 1
            yield scrapy.Request(url=listing_url,meta={'para': para_s, 'url': listing_url,"date_info":y}, callback=self.parse_details,dont_filter=True)


    def parse_details(selfself,response):
        date_info=response.meta['date_info']
        time1 = re.findall(r"\d+\.?\d*", date_info)
        time2 = re.findall(r'[A-Za-z]', date_info)

        para_ss = response.meta['para']
        basicurl=response.meta['url']
        pattern = re.compile(r'(?<=jobListingId=)\d+\.?\d*')
        x = pattern.findall(basicurl)
        jobid=x[0]



        html_data = response.text
        page_soup = soup(html_data, "html.parser")
        returned_tuple = extract_listing(page_soup)
        returned_tuple_list = list(returned_tuple)

        times = time.time()
        second_timestamp=int(times)

        if 'd' in time2[0]:
            a=int(time1[0])*24*3600
            second_timestamp_final=second_timestamp-a
        elif 'h' in time2[0]:
            b = int(time1[0]) * 3600
            second_timestamp_final=second_timestamp-b


        item = GlassdoorItem()
        item['company']=returned_tuple_list[0]
        item['locations']=returned_tuple_list[2]
        item['title']=returned_tuple_list[1]
        item['description']=returned_tuple_list[3]
        #item['job_category']=para_ss[0]
        #item['job_schedule_type']=para_ss[2]
        item['publish_time']=second_timestamp_final
        item['glassdoor_id']=jobid
        item['from_url']=basicurl
        #item update last ?? day

        yield item

