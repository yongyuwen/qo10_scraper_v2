# -*- coding: utf-8 -*-
import scrapy
import re
import math


class Qo10Spider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.qoo10.sg']
    start_urls = [
        'https://m.qoo10.sg/gmkt.inc/Mobile/search/brand.aspx?brandno=35286&brandnm=Kinohimitsu'
        # 'https://m.qoo10.sg/gmkt.inc/Mobile/Search/BrandAjaxAppend.aspx?gid=226776&page_type=search_query_new&page_size=50&page_no=1'
    ]

    '''page_urls = [
        'https://m.qoo10.sg/gmkt.inc/Mobile/Search/BrandAjaxAppend.aspx?gid=226776&page_type=search_query_new&page_size=50'
    ]'''

    def parse(self, response):
        # number_of_products = response.css('div.section_brand > div.grp_brdinfo > div.dtl > p > strong::text').extract()
        number_of_products = float(response.css('div.section_brand > div.grp_brdinfo > div.dtl > p > strong::text').re(r'\w+')[0])
        number_of_pages_to_scrape = math.ceil(number_of_products / 50)
        '''
        for page in range(1,number_of_pages_to_scrape+1):
            listing_page = self.page_urls[0] + "&page_no=" +str(page)
            yield response.follow(listing_page,self.parse_listing_page)
        '''
        pattern1 = '\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t'
        pattern2 = '\r\n\t\t\t\t\t\t\t'
        titles = response.css('h3.tt::text').extract()
        original_price = response.css('del::text').extract()
        discounted_price = response.css('div.prc > strong::text').extract()
        for i in range (0,len(titles)):
            titles[i] = re.sub(pattern1, "", titles[i])
            titles[i] = re.sub(pattern2, "", titles[i])


        scraped_info = {}
        # Give the extracted content row wise
        for item in zip(titles, original_price, discounted_price):
            # create a dictionary to store the scraped info
            scraped_info = {
                'title': item[0],
                'original_price': item[1],
                'discounted_price': item[2],
            }
            # yield or give the scraped info to scrapy
            yield scraped_info




