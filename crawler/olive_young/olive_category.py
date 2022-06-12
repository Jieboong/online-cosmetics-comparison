import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import csv, json

options = webdriver.ChromeOptions()

options.add_argument("headless")

# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

s = Service('chromedriver')

driver = webdriver.Chrome(service = s, options=options)

driver.get("https://www.oliveyoung.co.kr/store/main/main.do?oy=0")

driver.find_element(By.XPATH, '//*[@id="btnGnbOpen"]').click()

beauty = driver.find_element(By.XPATH, '//*[@id="gnbAllMenu"]/ul/li[1]')

cate_num = {}

big_category = beauty.find_elements(By.CLASS_NAME, "sub_depth")
for big in big_category : 
    cate_num[big.text] = {}
small_categories = beauty.find_elements(By.TAG_NAME, "ul")

for i in range(len(big_category)) : 
    small = small_categories[i]
    category = small.find_elements(By.TAG_NAME, 'li')
    for c in category : 
        small_category = c.find_element(By.TAG_NAME, 'a')
        cate_num[big_category[i].text][small_category.get_attribute('data-ref-dispcatno')] = small_category.text
with open ('./category.json','w', encoding='UTF-8') as fp :
    json.dump(cate_num, fp, ensure_ascii = False)

    
