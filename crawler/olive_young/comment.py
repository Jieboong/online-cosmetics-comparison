from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import json,csv
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

olive_url = 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo={dispatch}&pageIdx={page}&rowsPerPage=24'
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

options = webdriver.ChromeOptions()


options.add_argument("headless")

# options.add_experimental_option('excludeSwitches', ['enable-logging'])

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

s = Service('/Users/juhee/Desktop/2022/toonight/chromedriver')
driver = webdriver.Chrome(service = s, options=options)
driver.implicitly_wait(10)

with open("./olive_category.json") as json_file :
    json_data = json.load(json_file)

f = open("./from_the_top.csv", 'a+', newline='')
writer = csv.writer(f)


for bigCategory, smallCategory in json_data.items() :
    for categoryNumber, categoryName in smallCategory.items() :
        index = 1
        # 각 카테고리별 페이지 돌아가며 크롤링
        while True :
            cur_url = olive_url.format(dispatch=categoryNumber, page=index)
            try :
                driver.get(cur_url)
            except : 
                driver.get(cur_url)
            time.sleep(2)
            
            num = driver.find_element(By.XPATH, '//*[@id="Contents"]/p/span').text

            if num == '0' :
                break

            products = driver.find_elements(By.CLASS_NAME, 'prd_info')
            infos = []
            for product in products: 
                
                product_info = product.find_element(By.TAG_NAME, "a")
                product_id = product_info.get_attribute("data-ref-goodsno")
                product_url = product_info.get_attribute("href")

                infos.append((product_id, product_url))
            
            for product_id, product_url in infos:
                driver.get(product_url)
                time.sleep(2)
                
                p = False
                while not p :
                    try : 
                        review = driver.find_element(By.XPATH, '//*[@id="reviewInfo"]/a')
                        review.click()
                        p = True
                    except:
                        continue
                endButton = False
                page = 1

                time.sleep(2)
                while not endButton : 
                    print(page, product_url)
                    reviews = driver.find_elements(By.CLASS_NAME, "review_cont")
                
                    for review in reviews :

                        poll_types = review.find_elements(By.CLASS_NAME, 'poll_type1')
                    
                        try : 
                            review_text = review.find_element(By.CLASS_NAME,'txt_inner').text.replace('\n', '').replace('\t', '')
                        except : 
                            review_text= ''

                        writer.writerow([product_id,review_text])
                    isThisEnd = True

                    nxt_buttons = driver.find_element(By.CLASS_NAME, "pageing").find_elements(By.TAG_NAME, 'a')
                    
                    found= False
                    for nxt in nxt_buttons : 
                        if int(nxt.get_attribute('data-page-no')) == page+1 :
                            found= True
                            break
                    if found :
                        nxt.click()
                        time.sleep(1.5)
                        page+=1
                    else :
                        endButton = True
                    if page > 30 :
                        endButton = True
                driver.back()
                time.sleep(2)
            index += 1
driver.quit()
