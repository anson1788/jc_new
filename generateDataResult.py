from os import listdir
from os.path import isfile, isdir, join
import datetime
import json

mypath = "D:\\jc_new\\result"
files = listdir(mypath)


def sortable_date(item_dictionary):
    datetime_string = item_dictionary['matchTime']
    return datetime.datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S+08:00')


matchList =[]
for f in files:
    fullpath = join(mypath, f)
    fileNameTime = f.replace(".json", "")
    with open(fullpath) as json_file:
        data = json.load(json_file)
        for x in data["matches"]:
            if 'cornerresult' in x and x["cornerresult"]!="-":
                matchList.append(x)

matchSingleResult = []
for idx, x in enumerate(matchList):
    if not any(z["matchID"] in x["matchID"] for z in matchSingleResult):
        matchSingleResult.append(x)

matchSingleResult.sort(key=sortable_date)
resultDict = {}
for idx, x in enumerate(matchSingleResult):
    resultDict[x['matchID']] = x
    print(x['matchID'], x['matchTime'])


res = json.dumps(resultDict)
with open("combine/all.json", "w") as outfile:
     outfile.write(res)