# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 13:49:00 2022

@author: Anjali Chawda
"""
import numba
from numba import cuda
print(numba.__version__)

import selenium
import warnings
warnings.filterwarnings('ignore')

from selenium import webdriver                    #import webDriver
import warnings 
warnings.filterwarnings('ignore')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')        #remove this for easy debbuing on your laptop /pc
chrome_options.add_argument('--no-sandbox')                             
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)


# from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver_service = Service(executable_path= "C:\SeleniumDriver\chromedriver.exe")
driver = webdriver.Chrome()
driver.implicitly_wait(10)
# get the url
url = "https://www.youtube.com/"
driver.get(url)
driver.implicitly_wait(30)

search_element = driver.find_element(By.NAME, 'search_query')
search_element.click()
val = input("Enter your search here for analysis:  ")
search_element.send_keys(val + Keys.ENTER)
time.sleep(5)


driver.execute_script("window.scrollTo(0, 70000);")
titles = driver.find_elements(By.XPATH ,'//a[@id="video-title"]')
time.sleep(5)

print(len(titles))

def data(text):
    before_keyword, keyword, after_keyword = text.partition('by')
    list = text.split(' ')
    title = before_keyword.split(' ')[0:3]
    channel = after_keyword.split(' ')[1:2]
    views = (' ').join(list[-2:])

    return {'title': title,'channel':channel, 'views':views}


list = []
for i in range(len(titles)):
    
  dict = data(titles[i].get_attribute('aria-label'))  
  dict["url"] = titles[i].get_attribute('href')
  list.append(dict)

data = pd.DataFrame(list)
# printing shape of data:
print("Shape of the extracted video data: ",data.shape)

convert_dict = {'title': str,
                'channel': str}
data.astype(convert_dict)
data['views'] = data['views'].str.replace('views', '')
data['views'] = data['views'].str.replace(',', '')
data['views'] = data['views'].str.replace('play Short', '0')

data['views'] = pd.to_numeric(data['views'], errors= 'coerce')

# get the top video links based on top video views
data.sort_values('views', ascending = False, inplace = True)
print(data)

href = pd.DataFrame(data['url'][0:15]).reset_index()
href.drop(['index'],axis = 1,inplace = True)
print(href)