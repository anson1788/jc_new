import requests
import time
import json



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

