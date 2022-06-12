import json
import requests
from bs4 import BeautifulSoup
import time
import datetime


olive_url = 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo={dispatch}&pageIdx={page}&rowsPerPage=48'

with open("./category.json") as json_file :
    json_data = json.load(json_file)

data = []

for bigCategory, smallCategory in json_data.items() :
    for categoryNumber, categoryName in smallCategory.items() :
        index = 1
        # 각 카테고리별 페이지 돌아가며 크롤링
        while True :
            cur_url = olive_url.format(dispatch=categoryNumber, page=index)
            print(cur_url)
            p = False 
            while not p :
                try : 
                    res = requests.get(cur_url,headers ={"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36" })
                    p = True
                except:
                    continue
                
            soup = BeautifulSoup(res.text, 'html.parser')

            ## 마지막 페이지 도달했을 경우 break
            count = soup.select_one('#Contents > p > span').get_text().strip()  
            print(count)          
            if count == '0' :
                break

            ## 각 상품에 대한 내용 크롤링
            products = soup.find_all("div", {"class" : "prd_info"})
            
            for product in products :

                product_info  = product.find("div", "prd_name")
                id = product_info.find("a")["data-ref-goodsno"]
                brand = product_info.find("a").find("span").text
                name = product_info.find("a").find("p").text
                img = product.find("a").find("img")["src"]
                link = product.find("a")["href"]

                if product.find("a").find("span", "status_flag soldout") :
                    soldout = True
                else : 
                    soldout = False
                
                product_price = product.find("p", "prd_price")
                price = product_price.find("span", "tx_cur").find("span").text

                if product_price.find("span", "tx_org") :
                    original_price = product_price.find("span", "tx_org").find("span").text
                    on_discount = True
                else :
                    original_price = price
                    on_discount = False
                try : 
                    product_res = requests.get(link,headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"})
                except: 
                    continue
                product_bs = BeautifulSoup(product_res.text, 'html.parser')

                shipping_options = product_bs.find("ul", "bl_list").find_all("li")
                shipping = [ a.find("span").text for a in shipping_options]
                
                benefit_options = product_bs.find("div", "txt_list").find_all("p")
                benefit = [ a.text for a in benefit_options]

                color_info = {}
                color_option = []

                if product_bs.find("div", "prd_colorchip_list") :

                    color_list = product_bs.find("div", "prd_colorchip_list").find_all("thumb-color")
                    count = 0
                    for color in color_list : 
                        color_option.append(color.find("input", {"name" : "colrCmprItemNm_%d"%count})["value"])

                        count += 1
                color_info["count"] = count
                color_info["color_option"] = color_option
                
                cur_info = {
                    "id" : id,
                    "brand" : brand,
                    "name" : name,
                    "link" : link,
                    "soldout" : soldout,
                    "cur_price" : price,
                    "original_price" : original_price,
                    "on_discount" : on_discount,
                    "shipping" : shipping,
                    "payment_benefit" : benefit,
                    "color_options" : color_info,
                    "img" : img,
                    "big_category" : bigCategory,
                    "small_category" : categoryName
                }

                data.append(cur_info)
            index += 1
today = datetime.datetime.today().strftime("%Y%m%d")
with open ('./olive_%s.json'%today,'w', encoding='UTF-8') as fp :
    json.dump(data, fp, ensure_ascii = False)


