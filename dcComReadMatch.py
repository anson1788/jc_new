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

def isReturn(matchResult,target,mode):
    if mode == "OU":
        markOU = 999
        if(matchResult["OU"]["odd"]==target["OU"]["odd"]):
            home = float(target["OU"]["home"])-float(matchResult["OU"]["home"])
            away = float(target["OU"]["away"])-float(matchResult["OU"]["away"])
            if home<0.1 and away<0.1:
                markOU = math.sqrt(home**2 + away**2)
        return "{:.2f}".format(markOU)
    elif mode == "HC":
        markHandicap = 999
        if(matchResult["Handicap"]["odd"]==target["Handicap"]["odd"]):
            home = float(target["Handicap"]["home"])-float(matchResult["Handicap"]["home"])
            away = float(target["Handicap"]["away"])-float(matchResult["Handicap"]["away"])
            if home<0.1 and away<0.1:
                markHandicap =math.sqrt(home**2 + away**2)
        return "{:.2f}".format(markHandicap)
    else:
        markHandicap = 999
        if(matchResult["Handicap"]["odd"]==target["Handicap"]["odd"]):
            home = float(target["Handicap"]["home"])-float(matchResult["Handicap"]["home"])
            away = float(target["Handicap"]["away"])-float(matchResult["Handicap"]["away"])
            if home<0.1 and away<0.1:
                markHandicap =math.sqrt(home**2 + away**2)

        markOU = 999
        if(matchResult["OU"]["odd"]==target["OU"]["odd"]):
            home = float(target["OU"]["home"])-float(matchResult["OU"]["home"])
            away = float(target["OU"]["away"])-float(matchResult["OU"]["away"])
            if home<0.1 and away<0.1:
                markOU = math.sqrt(home**2 + away**2)
    
        if markOU !=999 and markHandicap==999:
            markHandicap = 1
        if markOU ==999 and markHandicap!=999:
            markOU = 1

        return "{:.2f}".format(markHandicap + markOU)

 



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

def isTargetMatch(singleMatch,targetMatch):
    if(singleMatch["result"]=="" and singleMatch["halfresult"]=="" and singleMatch["home"] == targetMatch["home"] and singleMatch["away"] == targetMatch["away"]):
        return True
    else:
        return False
        
def readTargetMatch(matchArr,targetMatch):
    resultArr =[]
    for singleTMatch in targetMatch:
        for idx, x in enumerate(matchArr):
            matchArr[x]["id"] = x
            matchArr[x]["matchTimeInSecound"] = datetime.strptime(matchArr[x]["matchTime"], "%Y-%m-%d %H:%M").timestamp()
            if isTargetMatch(matchArr[x],singleTMatch):
                resultArr.append(matchArr[x])
    return resultArr

def loopThroughMatch(matchArr,resultArr,mode):
    for singleTMatch in resultArr:
        resultList = readMatch(matchArr,singleTMatch,mode)
        inRange = []
        inScore = []
        for x in resultList:
            if float(x["mark"]) < 0.04:
                print(x)
                inRange.append(x)
                hhs = int(x["halfresult"].split("-")[0])
                has = int(x["halfresult"].split("-")[1])
                hts = hhs + has
                if hts > 0 : 
                    inScore.append(x)
        htp = 0
        if len(inRange) != 0 :
            htp =  float("{:.3f}".format(len(inScore)/len(inRange)))
        print(htp , " ",len(inScore) , " / ",len(inRange) )



def readMatch(inputData,targetMatch,mode):
    matchArr = inputData.copy()
    for idx, x in enumerate(matchArr):
        matchArr[x]["id"] = x
        matchArr[x]["matchTimeInSecound"] = datetime.strptime(matchArr[x]["matchTime"], "%Y-%m-%d %H:%M").timestamp()
        if(matchArr[x]["result"]!="" and matchArr[x]["halfresult"]!="" ):
            matchArr[x]["mark"] = isReturn(matchArr[x],targetMatch,mode)
            #del matchArr[x]["matchTimeInSecound"]
            #del matchArr[x]["Handicap"]
            #del matchArr[x]["OU"]
            #del matchArr[x]["round"]
            #del matchArr[x]["matchTime"]
            #del matchArr[x]["id"]
            listArr.append(matchArr[x])
    newlist = sorted(listArr, key=itemgetter('mark')) 
    dataset = newlist
    return newlist