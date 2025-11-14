# Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

import os
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests

# Initialize Chrome WebDriver
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
browser = webdriver.Chrome(options=options)

# Setup search parameters
city = "montreal"
product = "Iphone"
min_price = 0
max_price = 5000
days_listed = 60

# Setup base URL
url = f'https://www.facebook.com/marketplace/{city}/search?query={product}&minPrice={min_price}&maxPrice={max_price}&daysSinceListed={days_listed}&exact=false'

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

# Scroll down to load all results
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    
    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
    print("Scrolled..")

print("Finished scrolling, all results loaded...")
