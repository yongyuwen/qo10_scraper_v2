import scrapy
import re
import math
import requests
import json

product_dict = {}
id = "432028114"
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

print(product_dict)
'''
#http://www.compjour.org/tutorials/intro-to-python-requests-and-json/#the-response-object ####Response tutorials

##Script to save dict as json
with open('data.json', 'w') as fp:
    json.dump(data, fp)
    
print (type(jsonresponse))
for i in variation:
    print (i["sel_item_price"])

'''