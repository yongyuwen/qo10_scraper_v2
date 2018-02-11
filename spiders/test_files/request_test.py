# -*- coding: utf-8 -*-
import scrapy
import re
import math
import requests
import json


class Qo10Spider(scrapy.Spider):
    name = 'req'
    #allowed_domains = ['www.qoo10.sg']
    start_urls = [
        #'https://m.qoo10.sg/gmkt.inc/Mobile/search/brand.aspx?brandno=50798&brandnm=OBDESIGN'
        'https://www.qoo10.sg/item/2018-NEW-ARRIVAL-WINTER-SWEATER-THERMAL-JACKET-KOREAN-VERSION/432028114'
        #'https://www.qoo10.sg/gmkt.inc/search/brand.aspx?brandno=35286&brandnm=Kinohimitsu'
        #'https://m.qoo10.sg/gmkt.inc/Mobile/Search/BrandAjaxAppend.aspx?gid=226776&page_type=search_query_new&page_size=50&page_no=1'
    ]
    page_urls = [
        #'https://www.qoo10.sg/gmkt.inc/Search/SearchAjaxAppend.aspx?page_no=2&page_size=100&cix=0&keyword=&dispType=UIG4&sort_type=SORT_RANK_POINT&gdlc_cd=&gdmc_cd=&gdsc_cd=&brandgroup=0&priceMin=&priceMax=&brandno=50798&brandnm=OBDESIGN&gid=258407&group_code=&filterDelivery=NNNNNN&is_free_shipping_search=N&quick_delivery_yn=N&search_keyword=&search_type=BrandSearch'
        'https://www.qoo10.sg/gmkt.inc/Search/SearchAjaxAppend.aspx?page_no=2&page_size=100&cix=0&keyword=&dispType=UIG4&sort_type=SORT_RANK_POINT&gdlc_cd=&gdmc_cd=&gdsc_cd=&brandgroup=0&priceMin=&priceMax=&brandno=54650&brandnm=Shi%20Fu%20Ge&gid=211754&group_code=&filterDelivery=NNNNNN&is_free_shipping_search=N&quick_delivery_yn=N&search_keyword=&search_type=BrandSearch'
    ]


    def parse(self, response):
        #number_of_products = response.css('div.section_brand > div.grp_brdinfo > div.dtl > p > strong::text').extract()
        id = response.css('#gd_no::attr(value)').extract()[0]
        referer = "https://www.qoo10.sg/item/2018-NEW-ARRIVAL-WINTER-SWEATER-THERMAL-JACKET-KOREAN-VERSION/432028114"

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
                'Referer': referer,
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
                # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
            }

        )
        jsonresponse = r.json()
        variation = jsonresponse["d"]["Rows"]

        for model in variation:
            product_dict = {}
            product_dict["SKU ID"] = response.css('#gd_no::attr(value)').extract()
            product_dict["Product Name"] = [response.css('#goods_name::text').extract()[0].encode('utf-8')]
            product_dict["Url"] = response.css('link[rel="canonical"]::attr(href)').extract()
            product_dict["Retail Price"] = response.css('#ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_retailPricePanel > dl > dd::text').extract()
            product_dict["Q Price"] = response.css('#dl_sell_price > dd > strong::text').extract()
            product_dict["Discount Price"] = response.css('#ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_discount_info > dl > dd > strong::text').extract()
            product_dict["ModelNo"] = model["sel_no"]
            product_dict["VariationType1"] = model["sel_name1"]
            product_dict["VariationType2"] = model["sel_name2"]
            product_dict["VariationType3"] = model["sel_name3"]
            product_dict["VariationType4"] = model["sel_name4"]
            product_dict["VariationType5"] = model["sel_name5"]
            product_dict["Variation1"] = model["sel_value1"]
            product_dict["Variation2"] = model["sel_value2"]
            product_dict["Variation3"] = model["sel_value3"]
            product_dict["Variation4"] = model["sel_value4"]
            product_dict["Variation5"] = model["sel_value5"]
            product_dict["Quantity"] = model["remain_cnt"]
            product_dict["Additional Price"] = model["sel_item_price"]
            yield product_dict






        #dl_sell_price > dd > strong
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_discount_info > dl > dd > strong
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_retailPricePanel > dl > dd
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_retailPricePanel > dl > dd #retail price
        #dl_sell_price > dd > strong #Q-price
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_discount_info > dl > dd > strong #discount price










