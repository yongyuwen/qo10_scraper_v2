# -*- coding: utf-8 -*-
import scrapy
import re
import math
import requests
import json


class Qo10Spider(scrapy.Spider):
    name = 'sfg'
    #allowed_domains = ['www.qoo10.sg']
    start_urls = [
        #'https://m.qoo10.sg/gmkt.inc/Mobile/search/brand.aspx?brandno=50798&brandnm=OBDESIGN'
        'https://www.qoo10.sg/gmkt.inc/search/brand.aspx?brandno=54650&brandnm=Shi%20Fu%20Ge'
        #'https://www.qoo10.sg/gmkt.inc/search/brand.aspx?brandno=35286&brandnm=Kinohimitsu'
        #'https://m.qoo10.sg/gmkt.inc/Mobile/Search/BrandAjaxAppend.aspx?gid=226776&page_type=search_query_new&page_size=50&page_no=1'
    ]
    page_urls = [
        #'https://www.qoo10.sg/gmkt.inc/Search/SearchAjaxAppend.aspx?page_no=2&page_size=100&cix=0&keyword=&dispType=UIG4&sort_type=SORT_RANK_POINT&gdlc_cd=&gdmc_cd=&gdsc_cd=&brandgroup=0&priceMin=&priceMax=&brandno=50798&brandnm=OBDESIGN&gid=258407&group_code=&filterDelivery=NNNNNN&is_free_shipping_search=N&quick_delivery_yn=N&search_keyword=&search_type=BrandSearch'
        'https://www.qoo10.sg/gmkt.inc/Search/SearchAjaxAppend.aspx?page_no=2&page_size=100&cix=0&keyword=&dispType=UIG4&sort_type=SORT_RANK_POINT&gdlc_cd=&gdmc_cd=&gdsc_cd=&brandgroup=0&priceMin=&priceMax=&brandno=54650&brandnm=Shi%20Fu%20Ge&gid=211754&group_code=&filterDelivery=NNNNNN&is_free_shipping_search=N&quick_delivery_yn=N&search_keyword=&search_type=BrandSearch'
    ]


    def parse(self, response):
        #number_of_products = response.css('div.section_brand > div.grp_brdinfo > div.dtl > p > strong::text').extract()
        raw_no = response.css('#group_srch > div.dtl > p > strong::text').extract()
        raw_no[0] = re.sub(',', '', raw_no[0])
        raw_no[0] = re.sub(' ', '', raw_no[0])
        number_of_products = float(raw_no[0])
        number_of_pages_to_scrape = int(math.ceil(number_of_products/100))
        for page in range(1,number_of_pages_to_scrape+1):
            listing_page = self.page_urls[0].replace('page_no=2','page_no={0}').format(page)
            #listing_page = self.page_urls[0] + "&page_no=" +str(page)
            yield response.follow(listing_page, self.parse_listing_page)

    def parse_listing_page(self, response):
        raw_links = response.css('div > div.item > a::attr(href)').extract()
        raw_links = set(raw_links)
        final_links = list(raw_links)
        #raw_links = response.css('a::attr(href)').extract() for mobile site
        '''
        final_links = []
        for i in raw_links:
            if 'goodscode' in i:
                final_links.append(i)
        '''
        for product_page_url in final_links:
            yield response.follow(product_page_url, self.parse_product_page)

    def parse_product_page(self, response):
        pattern1 = '\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t'
        pattern2 = '\r\n\t\t\t\t'
        product_dict = {}
        '''
        product_dict["Product Name"] = response.css('div.section_goods > section.section_gdinfo > span::text').extract()[1]
        product_dict["Product Name"] = re.sub(pattern1, "", product_dict["Product Name"])
        product_dict["Product Name"] = re.sub(pattern2, "", product_dict["Product Name"])
        '''

        product_dict["SKU ID"] = response.css('#gd_no::attr(value)').extract()
        product_dict["Product Name"] = response.css('#goods_name::text').extract()
        product_dict["Url"] = response.css('link[rel="canonical"]::attr(href)').extract()
        #product_dict["Url"] = response.css('#ctl00_ctl00_Head2 > link:nth-child(15)::attr(href)').extract()
        yield product_dict








    ''' #Past inaccurate code
    def parse_listing_page(self, response):
        titles = response.css('h3.tt::text').extract()
        original_price = response.css('del::text').extract()
        discounted_price = response.css('div.prc > strong::text').extract()
        pattern1 = '\r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t'
        pattern2 = '\r\n\t\t\t\t\t\t\t'
        for i in range(0, len(titles)):
            titles[i] = re.sub(pattern1, "", titles[i])
            titles[i] = re.sub(pattern2, "", titles[i])

        scraped_info = {}

        for item in zip(titles, original_price, discounted_price):
            # create a dictionary to store the scraped info
            scraped_info = {
                'title': item[0],
                'original_price': item[1],
                'discounted_price': item[2],
            }
            # yield or give the scraped info to scrapy
            yield scraped_info
        '''

