import scrapy
import re
import math
import requests
import json
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

'''
product_dict = {}

url = 'https://www.qoo10.sg/item/BUY-2-FREE-SHIPPING-HIGH-QUALITY-JAPANESE-LINEN-APPARELS-COTTON/544852931'

r=requests.get(url)
body = r.text
search = re.findall(r"contents_no=([0-9]*?)&",body)

url = 'https://www.qoo10.sg/gmkt.inc/Goods/GoodsDetailInfo.aspx?contents_no=815743230&goodscode=544852931&global_order_type=L&org_des=N'

num0=815743230
num1=544852931

listing_page = 'https://www.qoo10.sg/gmkt.inc/Goods/GoodsDetailInfo.aspx?contents_no={0}&goodscode={1}&global_order_type=L&org_des=N'.format(num0,num1)




print (requests.get(url).text)
'''


'''
print (img)
print (len(img))
print (count)
'''
'''
img = Selector(text=body).css('img::attr(src)').extract()
        for i,j in zip()
        
        
        
img = Selector(text=body).css('img::attr(src)').extract()
count = list(range(1,len(img)+1))
dict = {}
for i,j in zip(count,img):
    dict['Image_{}'.format(i)]= j
'''
'''
url = 'https://www.qoo10.sg/gmkt.inc/Goods/GoodsDetailInfo.aspx?contents_no=867281574&goodscode=577269619&global_order_type=L&org_des=N'
r=requests.get(url)
body = r.text
list = Selector(text=body).css('div::text').extract()

print (list)
print('做戏之说')
'''

import urllib.parse
url = 'https://www.qoo10.sg/gmkt.inc/Search/SearchResultAjaxTemplate.aspx?minishop_bar_onoff=Y&sell_coupon_cust_no=OP9fAKT2lvDjPlthNZvTzQ==&SellerCooponDisplay=Y&sell_cust_no=OP9fAKT2lvDjPlthNZvTzQ%3D%3D&theme_sid=0&global_yn=N&qid=0&fbidx=-1&sortType=SORT_RANK_POINT&dispType=UIG4&filterDelivery=NNNNNANNNNNNNN&search_global_yn=N&shipto=ALL&is_research_yn=Y&coupon_filter_no=0&partial=on&paging_value=1&curPage=1&pageSize=120&ajax_search_type=M&___cache_expire___=1514456130289'
item = 'GizHmWRs+ZAWqAu0Br/A1Q=='
result = urllib.parse.quote_plus(item)

link = url.replace('sell_coupon_cust_no=OP9fAKT2lvDjPlthNZvTzQ==', 'sell_coupon_cust_no={}'.format(item))
link = url.replace('sell_cust_no=OP9fAKT2lvDjPlthNZvTzQ%3D%3D', 'sell_cust_no={}'.format(result) )
print (link)