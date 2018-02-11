# -*- coding: utf-8 -*-
import scrapy
import re
import math
import requests
import json
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


class Qo10Spider(scrapy.Spider):
    name = 'sing'
    #allowed_domains = ['www.qoo10.sg']
    start_urls = [
        #'https://m.qoo10.sg/gmkt.inc/Mobile/search/brand.aspx?brandno=50798&brandnm=OBDESIGN'
        'https://www.qoo10.sg/item/2018-NEW-ARRIVAL-WINTER-SWEATER-THERMAL-JACKET-KOREAN-VERSION/432028114'
        #***'https://www.qoo10.sg/gmkt.inc/Goods/Goods.aspx?goodscode=428137862' Chinese
        #'https://www.qoo10.sg/gmkt.inc/search/brand.aspx?brandno=35286&brandnm=Kinohimitsu'
        #'https://m.qoo10.sg/gmkt.inc/Mobile/Search/BrandAjaxAppend.aspx?gid=226776&page_type=search_query_new&page_size=50&page_no=1'
    ]
    page_urls = [
        #'https://www.qoo10.sg/gmkt.inc/Search/SearchAjaxAppend.aspx?page_no=2&page_size=100&cix=0&keyword=&dispType=UIG4&sort_type=SORT_RANK_POINT&gdlc_cd=&gdmc_cd=&gdsc_cd=&brandgroup=0&priceMin=&priceMax=&brandno=50798&brandnm=OBDESIGN&gid=258407&group_code=&filterDelivery=NNNNNN&is_free_shipping_search=N&quick_delivery_yn=N&search_keyword=&search_type=BrandSearch'
        'https://www.qoo10.sg/gmkt.inc/Search/SearchAjaxAppend.aspx?page_no=2&page_size=100&cix=0&keyword=&dispType=UIG4&sort_type=SORT_RANK_POINT&gdlc_cd=&gdmc_cd=&gdsc_cd=&brandgroup=0&priceMin=&priceMax=&brandno=54650&brandnm=Shi%20Fu%20Ge&gid=211754&group_code=&filterDelivery=NNNNNN&is_free_shipping_search=N&quick_delivery_yn=N&search_keyword=&search_type=BrandSearch'
    ]


    def parse(self, response):
        #number_of_products = response.css('div.section_brand > div.grp_brdinfo > div.dtl > p > strong::text').extract()
        product_dict = {}
        '''
        product_dict["Product Name"] = response.css('div.section_goods > section.section_gdinfo > span::text').extract()[1]
        product_dict["Product Name"] = re.sub(pattern1, "", product_dict["Product Name"])
        product_dict["Product Name"] = re.sub(pattern2, "", product_dict["Product Name"])
        '''

        product_dict["SKU ID"] = response.css('#gd_no::attr(value)').extract()
        product_dict["Product Name"] = response.css('#goods_name::text').extract()
        product_dict["Url"] = response.css('link[rel="canonical"]::attr(href)').extract()
        # product_dict["Url"] = response.css('#ctl00_ctl00_Head2 > link:nth-child(15)::attr(href)').extract()
        product_dict["Retail Price"] = response.css('#ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_retailPricePanel > dl > dd::text').extract()
        product_dict["Q Price"] = response.css('#dl_sell_price > dd > strong::text').extract()
        product_dict["Discount Price"] = response.css('#ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_discount_info > dl > dd > strong::text').extract()

        url = 'https://www.qoo10.sg/gmkt.inc/Goods/GoodsDetailInfo.aspx?contents_no=650356953&goodscode=432028114&global_order_type=L&org_des=N'
        r = requests.get(url)
        body = r.text
        info_1 = Selector(text=body).css('span::text').extract()
        info_2 = Selector(text=body).css('div::text').extract()
        info = info_1 + info_2
        s = " "
        info = s.join(info)
        product_dict['Info'] = info

        img = Selector(text=body).css('img::attr(src)').extract()
        count = list(range(1, len(img) + 1))
        dict = {}
        for i, j in zip(count, img):
            product_dict['Image_{}'.format(i)] = j

        yield product_dict










        #dl_sell_price > dd > strong
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_discount_info > dl > dd > strong
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_retailPricePanel > dl > dd
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_retailPricePanel > dl > dd #retail price
        #dl_sell_price > dd > strong #Q-price
        #ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_discount_info > dl > dd > strong #discount price










