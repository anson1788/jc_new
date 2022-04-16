import requests
import time
import json


#Simple assignment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path='C:\Windows\chromedriver.exe',options=chrome_options)
#driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',options=chrome_options)

loopIdx = 0
url ='https://bet.hkjc.com/football/odds/odds_chl.aspx?lang=ch'
driver.get(url)
time.sleep(5)
datas = driver.find_elements(by=By.CLASS_NAME,value='couponTable')
for data in datas:
    header=data.find_elements(by=By.CLASS_NAME,value="tgCoupon")
    obj=data.find_elements(by=By.CLASS_NAME, value=header[0].get_attribute("id"))
    for singleMatch in obj:
        inplay = singleMatch.find_elements(by=By.CLASS_NAME,value='inplayLnkInRow')
        inplaylen = len(inplay)
        if inplaylen > 0:
            alloddsLink = inplay[0].find_elements(by=By.CLASS_NAME,value='alloddsLink')
            alloddsLinklen = len(alloddsLink)
            if alloddsLinklen > 0:
                loopIdx = loopIdx + 1

driver.close()
print(loopIdx)

def getChl(url,params):
  s = requests.Session()
  resp = s.get(url=url, params=params)
  data = resp.json()
  return data



requestUrl = "https://bet.hkjc.com/football/getJSON.aspx?jsontype=results.aspx"

activeList = []
matchList = []
try:
    matchList = getChl(
        url=requestUrl,
        params=dict()
        )
except:
  time.sleep(10)
  matchList = getChl(
        url=requestUrl,
        params=dict()
        )

for idx, x in enumerate(matchList):
    if x["name"] == 'ActiveMatches':
        activeList = x

timestr = time.strftime("%Y%m%d-%H%M%S")

if len(activeList)>0:
    res = json.dumps(activeList)
    with open("result/"+timestr+".json", "w") as outfile:
        outfile.write(res)

