from dcComFunc import tryAgain
import dcComFunc
import dcComReadMatch
import json

config={}
'''
config["pageListUrl"]="https://zq.titan007.com/cn/League.aspx?SclassID=31"
config["match"]=[]

matchGame={}
matchGame["home"]="毕尔巴鄂竞技"
matchGame["away"]="奥萨苏纳"
matchGame["time"]="04:00"
config["match"].append(matchGame)
'''

config["pageListUrl"]="https://zq.titan007.com/cn/SubLeague/2021-2022/273_462.html"
config["match"]=[]

matchGame={}
matchGame["home"]="珀斯光荣"
matchGame["away"]="布里斯班狮吼"
matchGame["19:30"]="04:15"
config["match"].append(matchGame)

##result
matchArr = {}
##set config
dcComFunc.pageListUrl = config["pageListUrl"]
##start logic loop
for x in range(30):
    result = tryAgain(x,0)
    idx = result[0]
    matchArr = {**matchArr, **result[1]}
    if x >= idx:
        print(x)
        break
#matchArr = collections.OrderedDict(sorted(matchArr.items()))
#print(matchArr)

res = json.dumps(matchArr,ensure_ascii=False, indent=4)
with open("dcmac/match.json", "w",encoding="utf8") as outfile:
    outfile.write(res)

print("---start read match-----")
print("---start read match-----")
print("---start read match-----")
print("---start read match-----")
#targetArr = dcComReadMatch.readTargetMatch(matchArr,config["match"])
targetArr = [
    {
        "OU": {
            "home": "1.03",
            "odd": "2.5/3",
            "away": "0.83"
        },
        "halfresult": "",
        "round": "1",
        "matchTime": "2022-11-21 15:45",
        "home": "珀斯光荣",
        "away": "布里斯班狮吼",
        "Handicap": {
            "home": "0.98",
            "odd": "平/半",
            "away": "0.9"
        },
        "result": ""
    }
]
print("---start OU-----")
dcComReadMatch.loopThroughMatch(matchArr,targetArr,"OU")
print("---start HC-----")
dcComReadMatch.loopThroughMatch(matchArr,targetArr,"HC")
print("---start All-----")
dcComReadMatch.loopThroughMatch(matchArr,targetArr,"All")