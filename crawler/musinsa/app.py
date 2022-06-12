
from time import sleep, time
from bs4 import BeautifulSoup
import json
import requests
from multiprocessing import cpu_count, Pool
from contextlib import closing
import datetime

FILE_NAME=datetime.datetime.today().strftime("%Y%m%d")

# function to add to JSON
def write_json(new_data, filename=FILE_NAME+'.json'):
    with open(filename,'w+') as file:
        json.dump(new_data, file, ensure_ascii=False, indent = 4)
        
# Function to get all product links and stores in list
def getallProductLinks(i):
    links = []
    sleep(1) # 
    url = requests.get(f"https://www.musinsa.com/category/{i}")
    soup = BeautifulSoup(url.text, "html.parser")
    totalPage = int(soup.select_one("span.totalPagingNum").get_text())
    for j in range(1, totalPage+1):
        htmlPage = requests.get(f"https://www.musinsa.com/category/{i}?d_cat_cd=015&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=&page={j}&display_cnt=90&sale_goods=&group_sale=&kids=N&ex_soldout=&color=&price1=&price2=&exclusive_yn=&shoeSizeOption=&tags=&campaign_id=&timesale_yn=&q=&includeKeywords=&measure=",headers = {'User-Agent': 'Mozilla/5.0'})
        soup =  BeautifulSoup(htmlPage.text, "html.parser")
        for ultag in soup.find_all("ul", {"id": "searchList"}):
            for idx, litag in enumerate(ultag.find_all("li", {"class": "li_box"})):
                link = litag.find("a", {"class": "img-block"})['href']
                links.append(link)
                print("#No: ", idx)
    return links


def scrapePage(link):
    l = link
    try:
        sleep(0.5)   
        url = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0'})
        print(url.status_code)
        soup = BeautifulSoup(url.content, "html.parser")
        title = soup.find("span", {"class": "product_title"}).get_text().strip()
        category = soup.find("div", {"class": "product_info"}).find_all("a")[1].get_text()
        brand = soup.find("ul", {"class": "product_article"}).find("li").find("p", {"class": "product_article_contents"}).get_text().split()[0]
        image = soup.find("div", {"class": "product-img"}).find("img").get("src")
        sale = '0'
        try:
            sale = soup.find("span", {"class": "txt_kor_discount"}).get_text().strip()[:2]
            old_price = soup.find("span", {"class": "product_article_price"}).get_text().strip()
            new_price = soup.find("span", {"class": "txt_price_member"}).get_text().strip()
        except Exception as e:    
            old_price = soup.find("span", {"class": "product_article_price"}).get_text().strip()
            new_price = soup.find("span", {"class": "product_article_price"}).get_text().strip()
        try:
            optionData = soup.find("select").find_all("option")
            del optionData[0]
            option = []
            for k in optionData:
                option_data = {
                    "option": k.get('value'),
                    "stock": k.get('jaego_yn')
                }
                option.append(option_data)
        except Exception as e:
            option = []

        product_data = {
            "product_id" : link[-7:],
            "title": title,
            "category": category,
            "brand" : brand,
            "old_price" : old_price[:-1],
            "new_price" : new_price[:-1],
            "sale" : sale, 
            "category": category,
            "image" : f"https:{image}",
            "link" : link,
            "option" : option
        }
        return product_data
    except Exception as e:
        print(l)
        print(e)
    

if __name__ == "__main__":
    starttime = time()
    filename = "data.json"    

    html = requests.get("https://www.musinsa.com/category/015", headers = {'User-Agent': 'Mozilla/5.0'})
    bsObject = BeautifulSoup(html.text, "html.parser")
    categories = [x.find('a').get('data-code') for x in bsObject.find("div", {"id": "category_2depth_list"}).find_all("li")]
    
    links = []
    #Collecting products link to links list:
    """with closing(Pool(cpu_count())) as pool:
        items = pool.imap_unordered(getallProductLinks, categories)
        for i in items:
            links.extend(i)"""

    with open("link.json", 'r') as file:
        links = json.load(file)
    
    
    with closing(Pool(cpu_count())) as p:
        products = p.map(scrapePage, links['links'])
        write_json(products)

    print("time:", time()-starttime)
