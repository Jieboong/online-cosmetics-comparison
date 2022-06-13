from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random
#import boto3
from datetime import datetime
import re
import os.path

def crawlHasCategory(ID):
    baseUrl = "https://www.coupang.com/np/categories/" + str(ID) + "?listSize=60&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page={page}&channel=user&fromComponent=Y&selectedPlpKeepFilter=&sorter=bestAsc&filter=&component=486148&rating=0"
    ids = []
    products = []
    new_prices = []
    old_prices = []
    images = []
    href = []

    page = 1
    while page < 18 :
        url = baseUrl.format(page=page)
        print("page: %d" %page)
        try : 
            res = requests.get(url, timeout=10)
        except requests.exceptions.Timeout as e :
            continue
        time.sleep(random.uniform(0,0.5))

        soup = BeautifulSoup(res.content, 'html.parser')

        product_list = soup.find('ul', id='productList').find_all('li')
        
        ## 각 요소에 대해 아이디, 상품 이름, 용량, 개수 및 썸네일 이미지 파싱
        for product in product_list :
            link= product.find('a', class_='baby-product-link')
            ids.append(int(link['data-item-id']))
            href.append('https://www.coupang.com'+link['href'])
            images.append('https:'+link.find('img')['src'])
            products.append(product.find('div', class_='name').text.strip())
            if product.find('del', class_='base-price'):
                origin_price = re.sub(',','',product.find('del', class_='base-price').text.strip())
            else :
                origin_price = None
            if (product.select_one("div > span:nth-of-type(1)").text == "박스 훼손") or (product.select_one("div > span:nth-of-type(1)").text == "중고"):
                dis_price = re.sub(',','',product.select_one("div > strong:nth-of-type(2)").text.strip())
            else:
                dis_price = re.sub(',','',product.find('strong', class_='price-value').text.strip())
            old_prices.append(origin_price)
            new_prices.append(dis_price)
            
        time.sleep(random.uniform(0,0.5))
        print(url)
        page += 1

    name = []
    volume = []
    quantity = []

    for product in products : 
        splited = product.split(',')
        if len(splited) == 1:
            name.append(product)
            volume.append(None)
            quantity.append(None)
        elif len(splited) == 2: 
            name.append(splited[0])
            volume.append(None)
            quantity.append(splited[1])
        else :
            cur_volume = re.sub(r'[^0-9]', '',splited[1])
            cur_quantity = re.sub(r'[^0-9]','',splited[2])
            if cur_volume and cur_quantity: 
                name.append(splited[0])
                volume.append(int(cur_volume)*int(cur_quantity))
                quantity.append(int(cur_quantity))
            elif cur_quantity : 
                name.append(splited[0])
                volume.append(None)
                quantity.append(int(cur_quantity))
            elif cur_volume :
                name.append(splited[0])
                volume.append(int(cur_volume))
                quantity.append(None)
            else :
                name.append(product)
                volume.append(None)
                quantity.append(None)    

    coupang_df = pd.DataFrame(list(zip(ids, name, volume, quantity, old_prices, new_prices, images, href)), index=range(len(products)), columns=['id', 'name', 'volume', 'quantity', 'old_price', 'new_price', 'img_src', 'href'])
    today = datetime.today().strftime("%Y%m%d")
    coupang_df.to_csv("coupang{today}_{id}.csv".format(today=today, id=ID), index=False, encoding='utf-8-sig') # 상품명 한글 깨짐 방지

for i in range(176576, 176581): # 아이라이너 ~ 포인트리무버(아이팔레트 제외)
    crawlHasCategory(i) 
crawlHasCategory(403004) # 아이팔레트
