# -*- coding: utf-8 -*-
import scrapy
import re
import math
import requests
import json


class Qo10Spider(scrapy.Spider):
    name = 'qo10_'
    #allowed_domains = ['www.qoo10.sg']
    start_urls = [
        #'https://m.qoo10.sg/gmkt.inc/Mobile/search/brand.aspx?brandno=50798&brandnm=OBDESIGN'
        'https://www.qoo10.sg/gmkt.inc/search/brand.aspx?brandno=50798&brandnm=OBDESIGN'
        #'https://m.qoo10.sg/gmkt.inc/Mobile/Search/BrandAjaxAppend.aspx?gid=226776&page_type=search_query_new&page_size=50&page_no=1'
    ]
    page_urls = [
        'https://www.qoo10.sg/gmkt.inc/Search/SearchAjaxAppend.aspx?page_no=2&page_size=100&cix=0&keyword=&dispType=UIG4&sort_type=SORT_RANK_POINT&gdlc_cd=&gdmc_cd=&gdsc_cd=&brandgroup=0&priceMin=&priceMax=&brandno=50798&brandnm=OBDESIGN&gid=258407&group_code=&filterDelivery=NNNNNN&is_free_shipping_search=N&quick_delivery_yn=N&search_keyword=&search_type=BrandSearch'
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
        id = int(response.css('#gd_no::attr(value)').extract()[0])
        url = response.css('#ctl00_ctl00_Head2 > link:nth-child(15)::attr(href)').extract()[0]
        product_dict["SKU ID"] = response.css('#gd_no::attr(value)').extract()
        product_dict["Product Name"] = response.css('#goods_name::text').extract()

        #Get variation information
        if id == -1:
            product_dict["Variation"] = []
        else:
            search_request = {"inventory_no": "ST" + str(id), "lang_cd": "en", "inventory_yn": "",
                              "link_type": "N",
                              "gd_no": str(id), "global_order_type": "L",
                              "___cache_expire___": "1513939702435"}
            payload = json.dumps(search_request)

            r = requests.post(
                # url='http://list.qoo10.sg/gmkt.inc/swe_GoodsAjaxService.asmx/GetGoodsInventoryAvailableList',
                url='https://www.qoo10.sg/gmkt.inc/swe_GoodsAjaxService.asmx/GetGoodsInventoryAvailableList',
                data=payload,
                headers={  # 'Accept-Encoding': 'gzip, deflate',
                    'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept-Language': 'en-US,en;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/json',
                    # 'Host': 'list.qoo10.sg',
                    'Host': 'www.qoo10.sg',
                    # 'Origin': 'http://list.qoo10.sg',
                    'Origin': 'https://www.qoo10.sg',
                    'Referer': url,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
                    # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
                }

            )
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

