# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 11:27:41 2017

@author: Naveen
"""

# The wget module
import wget

import re
import time
import json

# The BeautifulSoup module
from bs4 import BeautifulSoup

# The selenium module
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.PhantomJS(
        executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
driver.get("https://s3.amazonaws.com/tripdata/index.html")

print("Page is loading.........")
WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="tbody-content"]/tr[1]/td[1]/a'))
) # waits till the element with the specific id appears

src = driver.page_source # gets the html source of the page

print("Done")


parser = BeautifulSoup(src,"lxml") 
# A list of attributes that you want to check in a tag
#list_of_attributes = {"class" : "some-class", "name" : "some-name"}
# Get the 'a' tag from the source
tag = parser.findAll('a')
len_tag = len(tag)
file_names={}
extracted = {}

file_path = 'C:/Users/Naveen/Downloads/Springboard/GitHub/new_york_citibikes/data/rides/file_names.json'
try:
    f = open(file_path, 'r')
    file_names = json.load(f)
    # if the file is empty the ValueError will be thrown
except ValueError:
    file_names = {}
except FileNotFoundError:#create file if not present
    f = open(file_path, 'w')
    f.close()
    f = open(file_path, 'r')
    file_names = json.load(f)
f.close()
    
    
for idx,i in enumerate(tag):
    url = i['href'] # get the href attribute of the video
    m = re.search('(?<=https://s3.amazonaws.com/tripdata/).*', url)
    
    if idx==len_tag-1:#check to skip index.html
        break
    
    if m.group(0) not in file_names:
        print("Downloading "+str(idx),end='\r',flush=True)
        wget.download(url,out="C:/Users/Naveen/Downloads/Springboard/GitHub/new_york_citibikes/data/rides/")
    file_names[m.group(0)] = 1

        
time.sleep(1)
print("")
print("All files downloaded")
    

# save to file:
with open('C:/Users/Naveen/Downloads/Springboard/GitHub/new_york_citibikes/data/rides/file_names.json', 'w') as f:
    json.dump(file_names, f)
    f.close()
    
driver.close()
driver.quit()