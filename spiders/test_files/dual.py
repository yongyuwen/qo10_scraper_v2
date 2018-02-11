# -*- coding: utf-8 -*-
import scrapy
import re
import math
import json


class Qo10Spider(scrapy.Spider):
    name = 'ddd'
    #allowed_domains = ['www.qoo10.sg']
    start_urls = [
        #'https://m.qoo10.sg/gmkt.inc/Mobile/search/brand.aspx?brandno=50798&brandnm=OBDESIGN'
        'https://www.qoo10.sg/item/2018-NEW-ARRIVAL-WINTER-SWEATER-THERMAL-JACKET-KOREAN-VERSION/432028114'
        #"https://www.qoo10.sg/gmkt.inc/Goods/GoodsDetailInfo.aspx?contents_no=650356953&goodscode=432028114&global_order_type=L&org_des=N"
        #'https://www.qoo10.sg/gmkt.inc/search/brand.aspx?brandno=35286&brandnm=Kinohimitsu'
        #'https://m.qoo10.sg/gmkt.inc/Mobile/Search/BrandAjaxAppend.aspx?gid=226776&page_type=search_query_new&page_size=50&page_no=1'
    ]



    def parse(self, response):
        product_dict = {}
        info = scrapy.Request('https://www.qoo10.sg/gmkt.inc/Goods/GoodsDetailInfo.aspx?contents_no=650356953&goodscode=432028114&global_order_type=L&org_des=N',
                        callback=self.search)
        print(type(info))
        product_dict['Info'] = info
        return product_dict

    def search(self, response):
        info_1 = response.css('span::text').extract()
        info_2 = response.css('div::text').extract()
        info = info_1 + info_2
        s = " "
        info = s.join(info)
        return info











        #dl_sell_price > dd > strong
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_discount_info > dl > dd > strong
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_retailPricePanel > dl > dd
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_retailPricePanel > dl > dd #retail price
        #dl_sell_price > dd > strong #Q-price
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_discount_info > dl > dd > strong #discount price










