#Simple assignment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import urllib.request
import os
import re
import json
import time
from datetime import datetime
from datetime import date
import collections
import traceback

os.system('pkill -f firefox')


#driver = webdriver.Chrome(executable_path='C:\Windows\chromedriver.exe',options=chrome_options)
driver = webdriver.Firefox(executable_path='/Users/hello/Desktop/chrome/geckodriver')


def loadPage(url):
    loopIdx = 0
    driver.set_page_load_timeout(10)
    try:
        driver.get(url)
        time.sleep(1)
    except Exception as e:
        print("keep")

loadPage("https://www.wabo11hk.com/")
