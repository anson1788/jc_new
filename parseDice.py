#Simple assignment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import urllib.request
import os
import time
from datetime import datetime
from os import listdir
from os.path import isfile, isdir, join
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option("detach", True)


mypath = "dice/"

files = listdir(mypath)


dataDict = {}
fileNameList = list()
for f in files:
    fullpath = join(mypath, f)
    fileName = f.replace(".json","")
    #print(fullpath," ",fileName)
    gameResult = []
    fileNameList.append(int(fileName))
    with open(fullpath) as json_file:
        data = json.load(json_file)
        dataDict[fileName] = data

fileNameList.sort()
onePlot = list()
twoPlot = list()
thrPlot = list()
fouPlot = list()
fivPlot = list()
sixPlot = list()
resList = list()
x = list()
xidx = 0
placeBet = 0
winBet = 0
dup = 0
for f in range(len(fileNameList)):
    idxData = fileNameList[f]
    isDuplicate = False
    if f>0:
        idxDataLst = fileNameList[f-1]
        if dataDict[str(idxData)]["1"] == dataDict[str(idxDataLst)]["1"] and \
        dataDict[str(idxData)]["2"] == dataDict[str(idxDataLst)]["2"] and \
        dataDict[str(idxData)]["3"] == dataDict[str(idxDataLst)]["3"] and \
        dataDict[str(idxData)]["4"] == dataDict[str(idxDataLst)]["4"] and \
        dataDict[str(idxData)]["5"] == dataDict[str(idxDataLst)]["5"] and \
        dataDict[str(idxData)]["6"] == dataDict[str(idxDataLst)]["6"] :
            isDuplicate =True
    print("------")
    if isDuplicate == False and f<len(fileNameList)-1:
        idxResult = fileNameList[f+1]
        gameResultData = dataDict[str(idxResult)]["result"][0]
        #print(resutl)
        x.append(xidx)
        xidx = xidx + 1
        onePlot.append(round(float(dataDict[str(idxData)]["1"]),2))
        twoPlot.append(round(float(dataDict[str(idxData)]["2"]),2))
        thrPlot.append(round(float(dataDict[str(idxData)]["3"]),2))
        fouPlot.append(round(float(dataDict[str(idxData)]["4"]),2))
        fivPlot.append(round(float(dataDict[str(idxData)]["5"]),2))
        sixPlot.append(round(float(dataDict[str(idxData)]["6"]),2))
        '''
        print("1 : ",round(float(dataDict[str(idxData)]["1"]),2))
        print("2 : ",round(float(dataDict[str(idxData)]["2"]),2))
        print("3 : ",round(float(dataDict[str(idxData)]["3"]),2))
        print("4 : ",round(float(dataDict[str(idxData)]["4"]),2))
        print("5 : ",round(float(dataDict[str(idxData)]["5"]),2))
        print("6 : ",round(float(dataDict[str(idxData)]["6"]),2))
        '''
        highlightIdx = "0"
        highlightVal = -1
        for y in ["1","2","3","4","5","6"]:
            print(round(float(dataDict[str(idxData)][y]),2))
            crtVal = round(float(dataDict[str(idxData)][y]),2)
            if crtVal < 25:
                if crtVal > highlightVal:
                    highlightIdx = y
                    highlightVal = round(float(dataDict[str(idxData)][y]),2)
        #print('highlight ',highlightVal)
     
        if highlightVal>17 and highlightVal<18:
            isContainTarget = False 
            isSecContainTarget = False
            for idxV in range(0,1):
                resultList = dataDict[str(idxData)]["result"]
                print(idxV,"?",dataDict[str(idxData)]["result"][idxV])
                if resultList[idxV][0] == highlightIdx or \
                resultList[idxV][1] == highlightIdx or \
                resultList[idxV][2] == highlightIdx :
                    isContainTarget = True
            for idxV in range(1,2):
                resultList = dataDict[str(idxData)]["result"]
                print(dataDict[str(idxData)]["result"][idxV])
                if resultList[idxV][0] == highlightIdx or \
                resultList[idxV][1] == highlightIdx or \
                resultList[idxV][2] == highlightIdx :
                    isSecContainTarget = True
            if isContainTarget == True and isSecContainTarget == False :
                print("Bet",highlightIdx)
                placeBet = placeBet + 1
                appearIdx = 0
                if gameResultData[0] == highlightIdx :
                    appearIdx = appearIdx + 1
                if gameResultData[1] == highlightIdx :
                    appearIdx = appearIdx + 1
                if gameResultData[2] == highlightIdx :
                    appearIdx = appearIdx + 1
                if gameResultData[0] == highlightIdx or \
                gameResultData[1] == highlightIdx or \
                gameResultData[2] == highlightIdx :
                        winBet = winBet + 1
                if appearIdx > 1:
                    dup = dup+ 1
print("placeBet :", placeBet , " winBet :",winBet, " dup : ",dup)


oneploy = np.array(onePlot)
twoploy = np.array(twoPlot)

#plt.plot(oneploy, 'o', color='green')
#plt.plot(x,twoploy, 'o', color='black')
#plt.legend()
#plt.show()