from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from datetime import datetime
import pandas as pd

# Khai báo browser
driver = webdriver.Chrome("D:\Py\crawl\chromedriver.exe")

allItems = []
#loop 30 site product 
for i in range(0,1):
    driver.get(f"https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.11035567?page={i}")
    total_height = 5000
    sleep(3)
    #smooth scroll to 5000px
    for j in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(j))
    sleep(2)
    allItem = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-xs-2-4 shopee-search-item-result__item']")))
    allItems.append(allItem)

# flatten array
allItems = [item for sublist in allItems for item in sublist]

for i in allItems:
    quatitys = i.find_elements(By.XPATH, "//div[@class='vbHrXG Rd0GDT']")
    prices = i.find_elements(By.XPATH,"//div[@class='_8nZsRt']")
    nameProduct = i.find_elements(By.XPATH,"//div[@class='TxwJWV _2qhlJo rrh06d']")
    # interactive = i.find_elements(By.XPATH,"//div[@class='_4vn1']")
list_quatity = [i.get_attribute("textContent") for i in quatitys]
list_price = [i.get_attribute("textContent") for i in prices]
list_name = [i.get_attribute("textContent") for i in nameProduct]

#process price
price, salePrice = [],[]
for i in list_price:
    char = re.findall("\d+\.\d+",i)
    # print(len(char))
    if len(char) == 1:
        price.append(char[0])
        salePrice.append(0)
    if len(char) == 2 and '-' not in i:
        salePrice.append(char[1])
        price.append(char[0])
    elif '-' in i:
        price.append(char[0])
        salePrice.append(0)

#process quantity sales
quantity_sale = sum([re.findall("\d+\,\d+k|\d+k|\d+",i) for i in list_quatity],[])

file_end = pd.DataFrame(list(zip(list_name,price,salePrice,quantity_sale)))
file_end.columns =['Tên sản phẩm', 'Giá gốc', 'Giá sale', 'Số lượng']
saveFile = file_end.to_csv('output_shopee.csv', encoding="utf-8-sig")
