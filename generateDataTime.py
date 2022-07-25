from os import listdir
from os.path import isfile, isdir, join
import datetime
import json
import pandas as pd

#mypath = "D:\\jc_new\\data"
#allJson = "D:\\jc_new\\combine\\all.json"
mypath = "/Users/hello/jc_new/data"
allJson = "/Users/hello/jc_new/combine/allNew.json"
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

for idx, x in enumerate(matchIDList):
    print(x , " ",idx)


pdResult = []
for idx, x in enumerate(matchIDList):
    timelineList = [] 
    timeStart = []
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

            timeStart.append(datetime.datetime.strptime(y["data"]["matchTime"], '%Y-%m-%dT%H:%M:%S+08:00'))
            cornerResult.append(y["data"]["cornerresult"])
            isSelling.append(y["data"]["chlodds"]["POOLSTATUS"])
            #print(y["data"]["chlodds"]["LINELIST"])
            for idxz,z in enumerate(y["data"]["chlodds"]["LINELIST"]):
                if z["MAINLINE"]=="true" :
                    oddPoint.append(z["LINE"].split("/")[0])
                    smallOddPoint.append(z["L"].replace("100@",""))
                    bigOddPoint.append(z["H"].replace("100@",""))
    
    for idxy, y in enumerate(timelineList):
        timelineListMinus.append(datetime.datetime.strptime(y, '%Y%m%d-%H%M%S'))
    

    for idxy, y in enumerate(timelineListMinus):
        min = (y-timeStart[0]).total_seconds()/60
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
    if isSelling[len(isSelling)-1]=="FinalStopSell":
        pdData = pd.DataFrame(data)
        #pdData.drop(pdData[pdData.Pool=="FinalStopSell"].index, inplace=True)
        pdData.drop(pdData[pdData.corner=="-1"].index, inplace=True)
        #pdData.drop(pdData[pdData.Pool=="NotSelling"].index, inplace=True)
        pdResult.append({
                "pd":pdData,
                "matchid":x
            })
    #print("-- ",len(timelineDiff)," ",len(cornerResult)," ",len(bigOddPoint)," ",len(oddPoint)," ",len(smallOddPoint))


gameResult = []
with open(allJson) as json_file:
    data = json.load(json_file)
    gameResult = data


for idx, x in enumerate(pdResult):
    if x["matchid"] in gameResult:
        data = {
            "time":[-1],
            "corner":[gameResult[x["matchid"]]["cornerresult"]],
            "High":[0],
            "Point":[0],
            "Low":[0],
            "Pool":[0]
        }
        pdData = pd.DataFrame(data)
        a = x["pd"]
        a.reset_index(drop=True, inplace=True)
        pdData.reset_index(drop=True, inplace=True)
        frames = [a, pdData]
        result = pd.concat(frames, axis=0,ignore_index=True)
        result.reset_index(drop=True)
        x["pd"] = result
        writer = pd.ExcelWriter("excel2/"+x["matchid"]+'.xlsx')
        x["pd"].to_excel(writer, index=False)
        writer.save()
        print(x["pd"])
    #print("----" , x["matchid"],idx)

print(len(pdResult))
