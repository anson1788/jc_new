import requests
import time
import json


#Simple assignment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def getChl(url,params):
  s = requests.Session()
  resp = s.get(url=url, params=params)
  data = resp.json()
  return data[1]



requestUrl = "https://bet.hkjc.com/football/getJSON.aspx?jsontype=odds_chl.aspx"

activeList = []
try:
    matchList = getChl(
        url=requestUrl,
        params=dict()
        )
    activeList = matchList["matches"]
except:
  time.sleep(10)
  matchList = getChl(
        url=requestUrl,
        params=dict()
        )
  activeList = matchList["matches"]

liveMatch = []   
for idx, x in enumerate(activeList):
    if x["inplaydelay"] == 'true':
    #if idx==0:
        liveMatch.append(x)
        print(idx, x['cornerresult'])

timestr = time.strftime("%Y%m%d-%H%M%S")

if len(liveMatch)>0:
    res = json.dumps(liveMatch)
    with open("data/"+timestr+".json", "w") as outfile:
        outfile.write(res)