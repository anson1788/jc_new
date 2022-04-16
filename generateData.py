from os import listdir
from os.path import isfile, isdir, join
import datetime
import json
import pandas as pd

mypath = "D:\jc_new\data"
files = listdir(mypath)



def sortable_date(item_dictionary):
    datetime_string = item_dictionary['time']
    return datetime.datetime.strptime(datetime_string, '%Y%m%d-%H%M%S')


dataList = []
for f in files:
    fullpath = join(mypath, f)
    fileNameTime = f.replace(".json", "")
    with open(fullpath) as json_file:
        data = json.load(json_file)
        for yIdx, y in enumerate(data):
            dataList.append({"time":fileNameTime,"data":y,"matchId":y["matchID"]})

dataList.sort(key=sortable_date)

matchIDList = []
for idx, x in enumerate(dataList):
    #print(x['data']['matchID'])
    if not any(z in x["data"]["matchID"] for z in matchIDList):
        matchIDList.append(x["data"]["matchID"])

#print(len(dataList))


pdResult = []
for idx, x in enumerate(matchIDList):
    timelineList = [] 
    timelineListMinus = []
    timelineDiff = []

    cornerResult = []
    oddPoint = []
    bigOddPoint = []
    smallOddPoint = []
    isSelling = []
    for idxy, y in enumerate(dataList):
        if y["matchId"] == x :
            timelineList.append(y["time"])
            cornerResult.append(y["data"]["cornerresult"])
            isSelling.append(y["data"]["chlodds"]["POOLSTATUS"])
            #print(y["data"]["chlodds"]["LINELIST"])
            for idxz,z in enumerate(y["data"]["chlodds"]["LINELIST"]):
                if z["MAINLINE"]=="true" :
                    oddPoint.append(z["LINE"])
                    smallOddPoint.append(z["L"].replace("100@",""))
                    bigOddPoint.append(z["H"].replace("100@",""))
    
    for idxy, y in enumerate(timelineList):
        timelineListMinus.append(datetime.datetime.strptime(y, '%Y%m%d-%H%M%S'))
    

    for idxy, y in enumerate(timelineListMinus):
        min = (y-timelineListMinus[0]).total_seconds()/60
        min = int(min)
        timelineDiff.append(min)
          
    data = {
        "time":timelineDiff,
        "corner":cornerResult,
        "High":bigOddPoint,
        "Point":oddPoint,
        "Low":smallOddPoint,
        "Pool":isSelling
    }
    pdData = pd.DataFrame(data)
    pdResult.append({
            "pd":pdData,
            "matchid":x
        })
    #print("-- ",len(timelineDiff)," ",len(cornerResult)," ",len(bigOddPoint)," ",len(oddPoint)," ",len(smallOddPoint))



print(len(pdResult))

gameResult = []
with open("D:\\jc_new\\combine\\all.json") as json_file:
    data = json.load(json_file)
    gameResult = data

print(gameResult)
for idx, x in enumerate(pdResult):
    if x["matchid"] in gameResult:
        print(x["pd"])