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
    resultArr = dataDict[str(idxData)]["result"]
    crtResult = resultArr[0]

    allDataArr = list()
    oneArr = list()
    twoArr = list()
    thrArr = list()
    forArr = list()
    fivArr = list()
    sixArr = list()
    def Average(lst):
        return sum(lst) / len(lst)
    for x in range(1,10):
        disArr = [0,0,0,0,0,0]
        for y in range(x,x+50):
        #for y in ["1","2","3","4","5","6"]:
            crtIdx = 0 
            for char in ["1","2","3","4","5","6"]:
                if resultArr[y][0] == char:
                    disArr[crtIdx] = disArr[crtIdx] + 1
                if resultArr[y][1] == char:
                    disArr[crtIdx] = disArr[crtIdx] + 1
                if resultArr[y][2] == char:
                    disArr[crtIdx] = disArr[crtIdx] + 1            
                crtIdx = crtIdx+1
        charPer = [0,0,0 , 0,0,0]
        for y in range(0,len(disArr)):
            charPer[y] = round(disArr[y]/((50-1)*3) *100,2)
        allDataArr.append(charPer)
        oneArr.append(charPer[0])
        twoArr.append(charPer[1])
        thrArr.append(charPer[2])
        forArr.append(charPer[3])
        fivArr.append(charPer[4])
        sixArr.append(charPer[5])
    dataList = [oneArr,twoArr,thrArr,forArr,fivArr,sixArr]
    for dls in dataList:
        print(Average(dls)-dls[0] , " mean :", Average(dls)," ",dls[0])
    print(" ",resultArr[0])
    print("-----")

    '''
    print(charPer[0]," ",charPer[1]," ",charPer[2]," ",charPer[3]," ",charPer[4]," ",charPer[5])
    highlightIdx = 0
    highlightVal = -1
    for y in range(len(charPer)):
        crtVal = charPer[y]
        if crtVal > highlightVal:
            highlightIdx = y
            highlightVal = crtVal
    #print(highlightIdx+1)
    highlightIdx = highlightIdx+1
    highlightIdx = str(highlightIdx)
    if highlightVal>10:
        isContainTarget = False 
        isSecContainTarget = False
        for idxV in range(1,2):
            resultList = resultArr[idxV]
            if resultList[0] == highlightIdx or \
            resultList[1] == highlightIdx or \
            resultList[2] == highlightIdx :
                isContainTarget = True      
        for idxV in range(2,3):
            resultList = resultArr[idxV]
            if resultList[0] == highlightIdx or \
            resultList[1] == highlightIdx or \
            resultList[2] == highlightIdx :
                isSecContainTarget = True   
        if isContainTarget == True and isSecContainTarget ==False:
            placeBet = placeBet + 1
            appearIdx = 0
            gameResultData = resultArr[0]
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
'''


#plt.plot(oneploy, 'o', color='green')
#plt.plot(x,twoploy, 'o', color='black')
#plt.legend()
#plt.show()