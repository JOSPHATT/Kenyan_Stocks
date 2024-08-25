import time
import json
import datetime
import os
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
options = webdriver.ChromeOptions()

options.add_argument('--headless')

options.add_argument('--no-sandbox')

options.add_argument('--disable-dev-shm-usage')

options.add_argument('--disable-gpu')

options.add_argument('--disable-features=NetworkService,NetworkServiceInProcess')

options.add_argument('--enable-javascript')



dr = webdriver.Chrome(options=options)
#https://www.betpawa.co.ke/upcoming?marketId=OU&categoryId=2

dr.get("https://www.tradingview.com/markets/stocks-kenya/market-movers-all-stocks/")

# Website used for scraping
dr.implicitly_wait(20)
elements = dr.find_elements(By.XPATH, "//*")
#print(len(elements))

info_raw={}
C=0
for element in elements:
    try:
        extracted_text = element.get_attribute('innerText')
        c=str(C)
        info_raw[c]=extracted_text
        C=C+1
    except:
        continue
#quitting the browser
dr.quit()

raw_info=info_raw["0"]
raw_info2 = raw_info.split('\n\n')
kenyan_stocks=raw_info2[1:54]
kenyan_stocks_dict={}
index_list=[0,1,3]
for stock in kenyan_stocks:
    k_stock=stock.split('\n')
    test_list = [i for i in k_stock if i]
    p_list=test_list[3]
    p_list2=p_list.split('\t')
    stock_info = test_list[0:2]+[p_list2[1]]
    kenyan_stocks_dict[stock_info[1]]=stock_info[2]
#print(kenyan_stocks_dict)

def final_data():
    return kenyan_stocks_dict
time_stamp=str(time.asctime())
Final_data={}  
Final_data[time_stamp]=final_data()
filename = '3hrly_kenyanstocks_prices.json'
entry = final_data()

if os.stat(filename).st_size == 0:
    with open(filename, "w") as file:
        json.dump(Final_data, file)
else:
    with open(filename, "r+") as file:
        data = json.loads(file)
        data[time_stamp]=entry
        file.seek(0)
        json.dump(data, file)
