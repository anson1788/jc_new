import requests
import time
import json


def getChl(url,params):
  resp = requests.get(url=url, params=params)
  data = resp.json()
  return data[1]



requestUrl = "https://bet.hkjc.com/football/getJSON.aspx?jsontype=odds_chl.aspx"

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