#################CHANGING OUTPUT FROM DIC TO JSON FORMAT AND APPENDING TO JSON"###############################
import time
import json
import datetime
import os
from selenium import webdriver
import requests
from bs4 import BeautifulSoup

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
for stock in kenyan_stocks:
    k_stock=stock.split('\n')
    test_list = [i for i in k_stock if i]
    p_list=test_list[3]
    p_list2=p_list.split('\t')
    stock_info = test_list[0:2]+[p_list2[1]]
    #print(stock_info)
    kenyan_stocks_dict[stock_info[1]]=stock_info[2]

time_stamp=str(time.asctime())
Final_data={} 
All_Kenya_stock_prices={}


# CHANGE 'kenyan_stocks_dict' by; ADD TIME/DATE , REMOVE 'KES' AND MAKE PRICES A FLOAT VARIABLE IN THE NESTED NEW DICT
def final_data():
    global kenyan_stocks_dict
    global time_stamp
    global Final_data
    for key, value in kenyan_stocks_dict.items():
    # Remove 'KES' and convert to float
        price = float(value.split()[0])  
    # Update the dictionary with the new value
        kenyan_stocks_dict[key] = price 
    Final_data[time_stamp]=kenyan_stocks_dict
  
    return Final_data
    
filename = '3hrly_kenyanstocks_prices.json'
new_stock_data = final_data()

# function to add to JSON
def write_json():
  global new_stock_data
  # Data to be written
  with open(filename, "w") as outfile:
    json.dump(new_stock_data, outfile)

def append_json(new_data, filename):
  global new_stock_data
  with open(filename,'r+') as file:
          # First we load existing data into a dict.
    file_data = json.load(file)
        # Join new_data with file_data inside emp_details
    file_data.update(new_data)
        # Sets file's current position at offset.
    file.seek(0)
        # convert back to json.
    json.dump(file_data, file, indent = 4)


###APPENDING OR INITIAliZING NEW FILE AND INITIAL DATA ENTRY INTO JSON FILE
# file_path to check whether it is empty
file_path = '3hrly_kenyanstocks_prices.json'
#checking whether file is empty
try:
    # get the size of file
    file_size = os.path.getsize(file_path)

    # if file size is 0, it is empty
    if (file_size == 0):
        print('JSON file is empty, WRITING FIRST DATA......')
        write_json(new_stock_data,filename)
            
    else:
          # if file size is not 0, it is not empty
        print('file is not empty, APPENDING DATA........')
        append_json(new_stock_data,filename)

# if file does not exist, then exception occurs
except FileNotFoundError as e:
    print('JSON File NOT found, CREATING NEW JSON FILE')
    f = open("3hrly_kenyanstocks_prices.json", "w")
    f.write(json.dumps(new_stock_data))
    f.close()

#########################################################################################################################
##BUSINESS NEWS FEEDS FUNCTION

# prompt1: code to extract news from  https://live.mystocks.co.ke/news.php
url1 = 'https://live.mystocks.co.ke/news.php'
response1 = requests.get(url1)

soup1 = BeautifulSoup(response1.content, 'html.parser')
news_articles = soup1.find_all('a', target="_blank")
news_publisher = soup1.find_all('i', {'class':"nPubl"})
news_date = soup1.find_all('i', {'class':"nDate"})

headline = []
publisher = []
dates = []
for article in news_articles:
    headline.append(article.text)
for pub in news_publisher:
    publisher.append(pub.text)
for dat in news_date:
    dates.append(dat.text)
#print(headline)
#print(publisher)
#print(dates)
kenyan_stocks_news = list(zip(headline,zip(publisher,dates)))

# prompt2: code to extract news from  'https://www.theeastafrican.co.ke/tea/business'
url2 = 'https://www.theeastafrican.co.ke/tea/business'
response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.content, 'html.parser')
east_african_news_articles =soup2.find_all('div', {'class':"five-eight column"})
east_african_news_articles_others = soup2.find_all('div', {'class':"sidebar-item"})
the_east_african_news_articles=east_african_news_articles_others+east_african_news_articles
the_east_african_news=[]
for article in the_east_african_news_articles:
    the_east_african_news.append(article.text)

# prompt3: code to extract news from  https://kenyanwallstreet.com/
url3 = 'https://kenyanwallstreet.com/'
response3 = requests.get(url3)
soup3 = BeautifulSoup(response3.content, 'html.parser')
kenyan_wall_street_news_articles =soup3.find_all('div', {'class':"jeg_block_container"})
kenyan_wall_street_news_articles_list=[]
for article in kenyan_wall_street_news_articles:
  kenyan_wall_street_news_articles_list.append(article.text)
kenyan_wall_street_news=kenyan_wall_street_news_articles_list

# prompt4: code to extract news from  https://www.businessdailyafrica.com/
url4 = 'https://www.businessdailyafrica.com/'
response4 = requests.get(url4)

soup4 = BeautifulSoup(response4.content, 'html.parser')
business_daily_news_articles =soup4.find_all('div', {'class':"grid-container-bd"})
business_daily_news=[]
for article in business_daily_news_articles:
  s=article.text
  s1= s.split('\n')
  for i in s1:
    if i=='':
      s1.remove(i)
    else:
      business_daily_news.append(i)

Collected_Business_News=kenyan_stocks_news+business_daily_news+the_east_african_news+kenyan_wall_street_news
#print(Collected_Business_News)
def news_feed():
    return Collected_Business_News
News_feeds={}  
News_feeds[time_stamp]=news_feed()
filename2 = 'Kenyan_stocks_news_feed.json'

with open(filename2, 'a') as outfile2:
    json.dump(News_feeds, outfile2)
#####################################################################################################################################



