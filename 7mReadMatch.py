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
import functools
from operator import itemgetter
import math
import tabulate

def isReturn(matchResult,target):
    '''
    markHandicap = 999
    if(matchResult["Handicap"]["odd"]==target["Handicap"]["odd"]):
       home = float(target["Handicap"]["home"])-float(matchResult["Handicap"]["home"])
       away = float(target["Handicap"]["away"])-float(matchResult["Handicap"]["away"])
       markHandicap =math.sqrt(home**2 + away**2)

    markOU = 999
    if(matchResult["OU"]["odd"]==target["OU"]["odd"]):
       home = float(target["OU"]["home"])-float(matchResult["OU"]["home"])
       away = float(target["OU"]["away"])-float(matchResult["OU"]["away"])
       markOU = math.sqrt(home**2 + away**2)
 
    if markOU !=999 and markHandicap==999:
        markHandicap = 1
    if markOU ==999 and markHandicap!=999:
        markOU = 1

    return "{:.2f}".format(markHandicap + markOU)
    '''    
    markOU = 999
    if(matchResult["OU"]["odd"]==target["OU"]["odd"]):
       home = float(target["OU"]["home"])-float(matchResult["OU"]["home"])
       away = float(target["OU"]["away"])-float(matchResult["OU"]["away"])
       markOU = math.sqrt(home**2 + away**2)
    return "{:.2f}".format(markOU)
    
    

 



os.system('pkill -f firefox')
with open("dcmac/match.json") as json_file:
    matchArr = json.load(json_file)

listArr = []
target = {
        "OU": {
            "home": "0.90",
            "odd": "2.5",
            "away": "0.96"
        },
        "halfresult": "",
        "round": "18",
        "matchTime": "2023-01-07 21:00",
        "home": "哈塔斯堡",
        "away": "安塔利亚体育",
        "Handicap": {
            "home": "1.05",
            "odd": "平手",
            "away": "0.83"
        },
}
for idx, x in enumerate(matchArr):
    matchArr[x]["id"] = x
    matchArr[x]["matchTimeInSecound"] = datetime.strptime(matchArr[x]["matchTime"], "%Y-%m-%d %H:%M").timestamp()
    if(matchArr[x]["result"]!="" and matchArr[x]["halfresult"]!="" ):
        matchArr[x]["mark"] = isReturn(matchArr[x],target)
        del matchArr[x]["matchTimeInSecound"]
        del matchArr[x]["Handicap"]
        del matchArr[x]["OU"]
        #del matchArr[x]["round"]
        del matchArr[x]["matchTime"]
        del matchArr[x]["id"]
        listArr.append(matchArr[x])


newlist = sorted(listArr, key=itemgetter('mark')) 
dataset = newlist
header = dataset[0].keys()
rows =  [x.values() for x in dataset]
print(tabulate.tabulate(rows, header, tablefmt='plain'))