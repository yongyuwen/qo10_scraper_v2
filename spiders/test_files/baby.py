# -*- coding: utf-8 -*-
import scrapy
import re
import math
import requests
import json
from scrapy.selector import Selector
import urllib.parse
import numpy


class Qo10Spider(scrapy.Spider):
    name = 'baby'
    # allowed_domains = ['www.qoo10.sg']
    start_urls = [
        # 'https://www.qoo10.sg/shop/andystrip'
        # 'https://www.qoo10.sg/shop/goodbuywee'
        'https://babyworldfair.com/starbuy/listing.html'
    ]

    page_urls = [
        #'https://babyworldfair.com/index.php?option=com_starbuy&view=get_detail&format=raw&id=4195'
        'https://babyworldfair.com/index.php?option=com_starbuy&view=get_detail&format=raw&id=1953'
    ]

    def parse(self, response):
        '''pages = np.array(list(range(0, 82)))
        page_no = pages * 12'''
        page_no = list(range(1953, 4196))

        for page in page_no:
            listing_page = self.page_urls[0].replace('id=1953', 'id={0}').format(page)
            yield response.follow(listing_page, self.parse_listing_page)

    def parse_listing_page(self, response):
        product_dict = {}
        product_dict["Item Name"] = response.css('body > div > div:nth-child(1) > div.starbuy_content_text > div > div.starbuy_p_name > a::text').extract_first()
        product_dict["Original Price"] = response.css('body > div > div:nth-child(1) > div.starbuy_content_text > div > span:nth-child(2)::text').extract_first().split(" :",1)[1]
        product_dict["Discount Price"] = response.css('body > div > div:nth-child(1) > div.starbuy_content_text > div > span:nth-child(4)::text').extract_first().split(": ",1)[1]
        yield product_dict
