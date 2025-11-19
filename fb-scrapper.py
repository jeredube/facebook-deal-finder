#!/usr/bin/env python
# coding: utf-8

# In[111]:


# Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import urllib.parse
import undetected_chromedriver as uc

import os
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests


# In[112]:


# Configure Chrome Webdriver

chrome_install = ChromeDriverManager().install()


# In[113]:


# Initialize Chrome WebDriver
options = webdriver.ChromeOptions()
#options.add_argument('--headless')

options.add_argument(
    "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)

browser = webdriver.Chrome(options=options)


# In[114]:


# Setup search parameters
city = "montreal"
product = "Gaming PC"
min_price = 0
max_price = 5000
days_listed = 7
MAX_SCROLLS = 4


# In[115]:


# Setup base URL
url = f'https://www.facebook.com/marketplace/{city}/search?query={product}&minPrice={min_price}&maxPrice={max_price}&daysSinceListed={days_listed}&sortBy=creation_time_descend&exact=false'

# Visit website
browser.get(url)

# Close login pop-up
try:
    close_button = browser.find_element(By.XPATH, "//div[@aria-label='Close']")
    close_button.click()
    print("Login prompt closed successfully...")
except:
    print("Login prompt not closed correctly...")
    pass


# In[116]:


# Scroll down to load all results
wait = WebDriverWait(browser, 10) # pause execution until condition is true w/ timotu limit

last_height = int(browser.execute_script("return document.body.scrollHeight"))
MIN_DELTA = 50  # minimum height change to count as "new content"

for i in range(MAX_SCROLLS):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.1)

    try:
        wait.until(
            lambda d: int(d.execute_script("return document.body.scrollHeight")) - last_height > MIN_DELTA
        )
        new_height = int(browser.execute_script("return document.body.scrollHeight"))
        print("Scroller successful:", new_height)
        last_height = new_height

    except TimeoutException:
        print("No further increase in scrollHeight. Stopping.")
        break

print("Finished Scrolling...")


# In[117]:


# Retrieve the HTML
html = browser.page_source

soup = BeautifulSoup(html, 'html.parser')

browser.close()


# In[118]:


# Find link elements
links = soup.find_all('a')

# Filter on product keyword only
product_links = [
    link for link in links
    if product.lower() in link.text.lower()
    #if city_link.lower() in link.text.lower()
]

product_data = []

for product_link in product_links:
    url = product_link.get('href')
    if not url:
        continue
    text = '\n'.join(product_link.stripped_strings)
    product_data.append({'url': url, 'text': text})


# In[119]:


# Create an empty list to store product data
extracted_data = []

for item in product_data:
    lines = item['text'].split('\n')

    # Regular expression to find numeric values
    numeric_pattern = re.compile('\d[\d,.]*')

    # Extracting prices
    # Iterate through lines to find the first line with numbers
    for line in lines:
        match = numeric_pattern.search(line)
        if match:    
            # Extract the first numeric value found
            price_str = match.group()
            # Convert price to float (handle commas)
            price = float(price_str.replace(',',''))
            break

    # Extract title
    title = lines[-2]

    # Extract location
    location = lines[-1]

    # Add extracted data to a list of dictionaries
    extracted_data.append({
        'title': title,
        'price': price,
        'location': location,
        'url': re.sub(r'\?.*', '', item['url'])
    })


# In[120]:


print(extracted_data)

