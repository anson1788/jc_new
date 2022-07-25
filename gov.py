#Simple assignment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
import sys
import urllib.request
import os
os.system('killall Google\ Chrome')
url='http://www.google.com'
print("---")
status_code = urllib.request.urlopen(url).getcode()
website_is_up = status_code == 400
print(website_is_up)
while website_is_up:
    status_code = urllib.request.urlopen(url).getcode()
    website_is_up = status_code == 200
    print(website_is_up)

import time
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option("detach", True)

#driver = webdriver.Chrome(executable_path='C:\Windows\chromedriver.exe',options=chrome_options)
driver = webdriver.Chrome(executable_path='/Users/hello/Desktop/chrome/chromedriver',options=chrome_options)



loopIdx = 0
url ='https://eapps2.td.gov.hk/repoes/td-es-app517/Start.do?language=zh'
driver.get(url)
datas = driver.find_elements(by=By.CLASS_NAME,value='captcha-code')
print(datas)
while(len(datas)!=1):
    datas = driver.find_elements(by=By.CLASS_NAME,value='captcha-code')

src = datas[0].get_attribute("src")

solver = TwoCaptcha('d4d73c05cf28b51baf6439f638d84080')
print("start solving")
try:
    result = solver.normal(src, caseSensitive=1)

except Exception as e:
    sys.exit(e)
print(result)
inputField = driver.find_elements(by=By.ID,value='solution')
print(inputField[0])
inputField[0].clear()
inputField[0].send_keys(result["code"])


btn = driver.find_elements(by=By.CLASS_NAME,value='botdetect-button')
print(btn)
while(len(btn)!=1):
    btn = driver.find_elements(by=By.CLASS_NAME,value='botdetect-button')

btn[0].click()