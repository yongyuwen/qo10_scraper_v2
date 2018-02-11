# -*- coding: utf-8 -*-
import scrapy
import re
import math
import requests
import json
from scrapy.selector import Selector
import urllib.parse


class Qo10Spider(scrapy.Spider):
    name = 'fuk'
    #allowed_domains = ['www.qoo10.sg']
    start_urls = [
        #'https://www.qoo10.sg/shop/andystrip'
        'https://www.qoo10.sg/shop/goodbuywee'
    ]

    page_urls = [
        'https://www.qoo10.sg/gmkt.inc/Search/SearchResultAjaxTemplate.aspx?minishop_bar_onoff=Y&sell_coupon_cust_no=OP9fAKT2lvDjPlthNZvTzQ==&SellerCooponDisplay=N&sell_cust_no=OP9fAKT2lvDjPlthNZvTzQ%3D%3D&theme_sid=0&global_yn=N&qid=0&search_mode=basic&fbidx=-1&sortType=SORT_RANK_POINT&dispType=UIG4&filterDelivery=NNNNNANNNNNNNN&search_global_yn=N&shipto=ALL&is_research_yn=Y&coupon_filter_no=0&partial=on&paging_value=1&curPage=1&pageSize=120&ajax_search_type=M&___cache_expire___=1514458016230'

    ]



    def parse(self, response):
        #Grab shop code
        shop_code = response.css('input[id="sell_coupon_cust_no"]::attr(value)').extract_first()
        result = urllib.parse.quote_plus(shop_code)
        link = self.page_urls[0].replace('sell_coupon_cust_no=OP9fAKT2lvDjPlthNZvTzQ==', 'sell_coupon_cust_no={}'.format(shop_code))
        link = self.page_urls[0].replace('sell_cust_no=OP9fAKT2lvDjPlthNZvTzQ%3D%3D', 'sell_cust_no={}'.format(result))


        #Grab number of pages
        raw_no = response.css('#btn_allitem > span::text').extract()
        number_of_products = float(raw_no[0])
        number_of_pages_to_scrape = int(math.ceil(number_of_products/120))
        for page in range(1,number_of_pages_to_scrape+1):
            listing_page = link.replace('curPage=1','curPage={0}').format(page)
            #listing_page = self.page_urls[0] + "&page_no=" +str(page)
            yield response.follow(listing_page, self.parse_listing_page)

    def parse_listing_page(self, response):
        raw_links = response.css('div > div.item > a::attr(href)').extract()
        raw_links = set(raw_links)
        final_links = list(raw_links)

        for product_page_url in final_links:
            yield response.follow(product_page_url, self.parse_product_page)

    def parse_product_page(self, response):

        product_dict = {}


        #Get price
        groupbuy = response.css('div[class="goods_type"]').extract_first()
        if groupbuy is None:
            retail_price = response.css(
                '#ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_retailPricePanel > dl > dd::text').extract()
            q_price = response.css('#dl_sell_price > dd > strong::text').extract()
            discount_price = response.css(
                '#ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_discount_info > dl > dd > strong::text').extract()
        else:
            retail_price = response.css('#goodsForm > div.goodsDetailWrap > div.goods_info > div.goods_detail > div.grpbuy_area > div.prc > del::text').extract_first()
            discount_price = response.css('#goodsForm > div.goodsDetailWrap > div.goods_info > div.goods_detail > div.grpbuy_area > div.prc > strong::text').extract_first()
            q_price = None



        #-----------------------------Get table-------------------------

        id = response.css('#gd_no::attr(value)').extract()[0]
        referer = response.css('link[rel="canonical"]::attr(href)').extract_first()
        #referer = "https://www.qoo10.sg/item/2018-NEW-ARRIVAL-WINTER-SWEATER-THERMAL-JACKET-KOREAN-VERSION/432028114"

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
        #-----------------------End of getting table--------------------

        #------------------------Get Description ---------------------------

        body = response.text
        contents_no = re.findall(r"contents_no=([0-9]*?)&", body)[0]


        desc_url = 'https://www.qoo10.sg/gmkt.inc/Goods/GoodsDetailInfo.aspx?contents_no={0}&goodscode={1}&global_order_type=L&org_des=N'.format(contents_no,id)
        desc = requests.get(desc_url).text

        #Get text
        info_1 = Selector(text=desc).css('span::text').extract()
        info_2 = Selector(text=desc).css('div::text').extract()
        info = info_1 + info_2
        s = " "
        info = s.join(info)

        #Get images
        img = Selector(text=desc).css('img::attr(src)').extract()
        count = list(range(1, 10))
        #count = list(range(1, len(img) + 1))




        for model in variation:

            product_dict["SKU ID"] = response.css('#gd_no::attr(value)').extract()
            #product_dict["Product Name"] = [response.css('#goods_name::text').extract()[0].encode('utf-8')]
            product_dict["Product Name"] = response.css('#goods_name::text').extract()
            product_dict["Url"] = response.css('link[rel="canonical"]::attr(href)').extract()
            product_dict["Display Image"] = response.css('img[id="GoodsImage"]::attr(content)').extract_first()
            product_dict["Retail Price"] = retail_price
            product_dict["Q Price"] = q_price
            product_dict["Discount Price"] = discount_price
            product_dict["Shipping From"] = response.css('td[colspan="3"]::text').extract_first()
            product_dict["Brief Description"] = response.css('td[itemprop="description"]::text').extract_first()
            product_dict['Info'] = info
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

            #Grab all desc images
            for i, j in zip(count, img):
                product_dict['Image_{}'.format(i)] = j

            yield product_dict









