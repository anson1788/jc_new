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
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option("detach", True)

os.system('killall Google\ Chrome')


#driver = webdriver.Chrome(executable_path='C:\Windows\chromedriver.exe',options=chrome_options)
driver = webdriver.Chrome(executable_path='/Users/hello/Desktop/chrome/chromedriver107',options=chrome_options)

progStartTime = datetime.now()

houseUrl = "https://bpweb.fuximex555.com/player/singleSicTable.jsp?dm=1&t=51&title=1&sgt=4&hall=1&mute=1"
#houseUrl = "https://bpweb.fuximex555.com/player/singleSicTable.jsp?dm=1&t=551&title=1&sgt=4&hall=4&mute=1"

def playSound():
  os.system('afplay sound/bet.wav &')

#playSound()


loopIdx = 0
url ='https://www.dc239.com'
driver.set_page_load_timeout(10)
try:
    driver.get(url)
except Exception as e:
    print("keep")

btn = driver.find_elements(by=By.CLASS_NAME,value='close')
while(len(btn)==0):
    #print("get btn")
    btn = driver.find_elements(by=By.CLASS_NAME,value='close')
time.sleep(1)
btn[0].click()


username = driver.find_elements(by=By.CLASS_NAME,value='username-btn')
while(len(username)==0):
    #print("username")
    username = driver.find_elements(by=By.CLASS_NAME,value='username-btn')
username[0].send_keys("anson1788")

password = driver.find_elements(by=By.CLASS_NAME,value='password-btn')
while(len(password)==0):
    password = driver.find_elements(by=By.CLASS_NAME,value='password-btn')
password[0].send_keys("Yu24163914")


login = driver.find_elements(by=By.CLASS_NAME,value='login')
while(len(login)!=1):
    login = driver.find_elements(by=By.CLASS_NAME,value='login')
login[0].click()

btn = driver.find_elements(by=By.CLASS_NAME,value='mps-close')
while(len(btn)!=1):
    btn = driver.find_elements(by=By.CLASS_NAME,value='mps-close')
btn[0].click()




url ='https://www.dc239.com/gamelobby/sports'
time.sleep(1)

matchItemkey = "讓球&amp;大小"
try:
    driver.get(url)
except Exception as e:
    print("keep")

submenu = driver.find_elements(by=By.CLASS_NAME,value='btn-main')
while(len(submenu)==0):
    submenu = driver.find_elements(by=By.CLASS_NAME,value='btn-main')

submenu[0].click()  

matchDict = {}
Whandles = driver.window_handles
driver.switch_to.window(Whandles[1])
print(Whandles)
time.sleep(5)


def runAllLiveMatch(driver,time):
    driver.get("https://c60prodpc.jyurpdy.cn/inplay/soccer") 
    time.sleep(2)
    looplist = list()
    matchList = driver.find_elements(by=By.CLASS_NAME,value='matchs-asia')
    leagueList = matchList[0].find_elements(by=By.CLASS_NAME,value='league-list')
    for x in leagueList:
        league = x.find_elements(by=By.CLASS_NAME,value='league-name')[0].get_attribute('innerHTML')
        if '電競' not in league:
            status = x.find_elements(by=By.CLASS_NAME,value='start-date')[0].find_elements(by=By.XPATH,value='span')[0].get_attribute('innerHTML')
            if '下半場' in status:
                matchTime = status.split(" ")[1]
                matchTime = matchTime.split(":")[0]
                if int(matchTime) > 60:
                    gameId = x.find_elements(by=By.CLASS_NAME,value='match-wrapper')[0].get_attribute('gidm')
                    looplist.append(gameId)
    for x in looplist:
        targetUrl = "https://c60prodpc.jyurpdy.cn/detail/"+x
        print(targetUrl)
        driver.get(targetUrl) 
        time.sleep(2)
        corner = True
        oddItem = driver.find_elements(by=By.CLASS_NAME,value='tabs-container')[0]
        oddName = oddItem.find_elements(by=By.CLASS_NAME,value='standard-disc-item')
        for y in oddName:
            ItemName = y.find_elements(by=By.CLASS_NAME,value='nav-rourd-icon')[0].get_attribute('innerHTML')
            if matchItemkey in ItemName.strip():
                corner = True
        if corner == True:
            matchProgress = driver.find_elements(by=By.CLASS_NAME,value='match-support-progress')[0]
            matchItem = matchProgress.find_elements(by=By.CLASS_NAME,value='support-progress-item')
            for y in matchItem:
                scoreContent = y.find_elements(by=By.CLASS_NAME,value='score')[0].get_attribute('innerHTML')
                if matchItemkey in scoreContent:
                    cornerRatio = scoreContent.split(" ")[1]
                    home = cornerRatio.split(":")[0]
                    away = cornerRatio.split(":")[1]
                    total = int(home) + int(away)
                print(scoreContent)
            middleList = driver.find_elements(by=By.CLASS_NAME,value='middle-matchList-component')[0]
            betlist = middleList.find_elements(by=By.CLASS_NAME,value='middle-matchList-list')
            for y in betlist:
                y.find_elements(by=By.CLASS_NAME,value='option-name')
                print("----")
                title = y.find_elements(by=By.CLASS_NAME,value='match-item')[0].find_elements(by=By.CLASS_NAME,value='option-name')[0]
                playtype = title.get_attribute("playtype")
                if len(playtype) > 1 :
                    print("ass")
                    playtype = y.find_elements(by=By.CLASS_NAME,value='option-name')[0].get_attribute('playtype')
                    print(playtype)
                '''
                if "ROU" in  playtype:
                  ratio = y.find_elements(by=By.CLASS_NAME,value='ratio')[0].get_attribute('innerHTML')
                  print(ratio)
                '''
#runAllLiveMatch(driver,time)
def runAllEarlyMatch(driver,time,url,isToday,matchDict):
    driver.get(url) 
    time.sleep(2)
    looplist = list()
    matchList = driver.find_elements(by=By.CLASS_NAME,value='matchs-asia')
    leagueList = driver.find_elements(by=By.CLASS_NAME,value='league-list')
    idx = 0
    while(len(leagueList)==0 and idx < 10):
        time.sleep(1)
        leagueList = driver.find_elements(by=By.CLASS_NAME,value='league-list')
        idx = idx + 1
    for x in leagueList:
        matchArr = {}
        league = x.find_elements(by=By.CLASS_NAME,value='league-name')[0].get_attribute('innerHTML')
        if '電競' not in league:
            status = x.find_elements(by=By.CLASS_NAME,value='start-date')[0].find_elements(by=By.XPATH,value='span')[0].get_attribute('innerHTML')
            home = x.find_elements(by=By.CLASS_NAME,value='team-name')[0].get_attribute('innerHTML')
            away = x.find_elements(by=By.CLASS_NAME,value='team-name')[1].get_attribute('innerHTML')
            statusDetails = status.split(" ")
            if isToday is True:
                #print("run today " ,statusDetails )
                if len(statusDetails) == 2:
                    gameId = x.find_elements(by=By.CLASS_NAME,value='match-wrapper')[0].get_attribute('gidm')
                    #looplist.append(gameId)  
                    matchArr["gameId"] = gameId
                    matchArr["home"] = home
                    matchArr["away"] = away
                    matchTime = str(date.today().year)+"-"+statusDetails[0].strip()+" "+statusDetails[1].strip()
                    matchArr["time"] = matchTime
                    t1 = datetime.strptime(matchTime, "%Y-%m-%d %H:%M")
                    diffInS = ( t1-datetime.now()).total_seconds()/3600
                    if diffInS < 3 :
                        looplist.append(gameId)  
                        matchDict[gameId] = {}
                        matchDict[gameId] = matchArr
                    #print('Start time:', t1.time(), " " ,diffInS)
                    #print(home,"-",away," ",statusDetails[0], " ",statusDetails[1])
            else:
                gameId = x.find_elements(by=By.CLASS_NAME,value='match-wrapper')[0].get_attribute('gidm')
                #print(home,"-",away," ",len(statusDetails))
    if isToday is False:
        print("monitor Match")
        print(matchDict)
        for key, value in matchDict.items() :
            matchTime = matchDict[key]["time"] 
            t1 = datetime.strptime(matchTime, "%Y-%m-%d %H:%M")
            diffInS = (datetime.now()-t1).total_seconds()/60
            if diffInS > 0 :
                looplist.append(key)
            else :
                print(diffInS)
        print("monitor Match end")
    for x in looplist:
        time.sleep(5)  
        targetUrl = "https://c60prodpc.jyurpdy.cn/detail/"+x
        driver.get(targetUrl) 
        time.sleep(2)  
        corner = False
        oddItem = driver.find_elements(by=By.CLASS_NAME,value='tabs-container')[0]
        league = driver.find_elements(by=By.CLASS_NAME,value='match-zone-name')[0].get_attribute('innerHTML')
        print("league ", league)
        oddName = oddItem.find_elements(by=By.CLASS_NAME,value='standard-disc-item')
        for y in oddName:
            ItemName = y.find_elements(by=By.CLASS_NAME,value='nav-rourd-icon')[0].get_attribute('innerHTML')
            if matchItemkey in ItemName.strip():
                corner = True
                y.click()
                middleMatch = driver.find_elements(by=By.CLASS_NAME,value='middle-matchList-component')[0]
                middeList = middleMatch.find_elements(by=By.CLASS_NAME,value='middle-matchList-list')
                for z in middeList:
                    matchListName = z.find_elements(by=By.CLASS_NAME,value='option-name')[0].get_attribute('innerHTML')
                    if isToday == True and '進球:大/小' in matchListName.strip() and '半場' not in matchListName.strip():
                        optionPanel = z.find_elements(by=By.CLASS_NAME,value='option-pannel')
                        option1 = optionPanel[0].find_elements(by=By.CLASS_NAME,value='option-group')[0]
                        ratio = option1.find_elements(by=By.CLASS_NAME,value='ratio')[0].get_attribute('innerHTML')
                        odd = option1.find_elements(by=By.CLASS_NAME,value='odds')[0].get_attribute('innerHTML')
                        oddD=re.findall("\d+\.\d+",odd)[0]
                        #print(ratio.strip().replace("大 ", " ") , "-", oddD.strip())
                        matchDict[x]["ratio"] = ratio.strip().replace("大 ", " ")
                        matchDict[x]["odd"] = oddD.strip()
                        matchDict[x]["league"] = league
                    elif isToday == False and '進球:大/小' in matchListName.strip() and '半場' in matchListName.strip():
                        optionPanel = z.find_elements(by=By.CLASS_NAME,value='option-pannel')
                        option1 = optionPanel[0].find_elements(by=By.CLASS_NAME,value='option-group')[0]
                        ratio = option1.find_elements(by=By.CLASS_NAME,value='ratio')[0].get_attribute('innerHTML')
                        odd = option1.find_elements(by=By.CLASS_NAME,value='odds')[0].get_attribute('innerHTML')
                        oddD=re.findall("\d+\.\d+",odd)[0]
                        print(ratio.strip().replace("大 ", " ") , "-", oddD.strip())
        #if corner == True:  
            #print(targetUrl) 

def triggerLoopAction(isLiveMatch, isToday):
    matchDict = {}
    with open("dcmac/match.json") as json_file:
        data = json.load(json_file)
    matchDict = data
    deleteList = []
    for key, value in matchDict.items() :
        matchTime = matchDict[key]["time"] 
        t1 = datetime.strptime(matchTime, "%Y-%m-%d %H:%M")
        diffInS = ( t1-datetime.now()).total_seconds()/3600
        if diffInS < -3:
            deleteList.append(key)
    for x in deleteList:
        del matchDict[x]

    if isToday:
        runAllEarlyMatch(driver,time,"https://c60prodpc.jyurpdy.cn/matchs/soccer/today",True,matchDict)                  
        runAllEarlyMatch(driver,time,"https://c60prodpc.jyurpdy.cn/matchs/soccer/early",True,matchDict)
        deleteList = []
        for key, value in matchDict.items() :
            ratio = matchDict[key]["ratio"] 
            matchRatio = ratio.split("/")[0]
            if float(matchRatio) >= 2.5:
                print (ratio, " ",  matchDict[key]["odd"]," ",matchDict[key]["time"] )
            else:
                deleteList.append(key)
        for x in deleteList:
            del matchDict[x]
            
    if isLiveMatch:
        runAllEarlyMatch(driver,time,"https://c60prodpc.jyurpdy.cn/inplay/soccer",False,matchDict)

    if isToday:
        res = json.dumps(matchDict,ensure_ascii=False, indent=4)
        with open("dcmac/match.json", "w",encoding="utf8") as outfile:
            outfile.write(res)

allMatchStart = True
liveMatchStart = True
allMatch = datetime.now()
liveMatch = datetime.now()

while True:
      diffInAllMatch = (datetime.now()-allMatch).total_seconds()/60
      if(diffInAllMatch>60 or allMatchStart):
        print("run all match")
        allMatch = datetime.now()
        triggerLoopAction(False,True)
        allMatchStart = False   

      diffInLiveMatch = (datetime.now()-liveMatch).total_seconds()
      if(diffInLiveMatch>120 or liveMatchStart):
        print("run live match")
        liveMatch = datetime.now()
        #triggerLoopAction(True,False)
        liveMatchStart = False
      print("single round complete")
      time.sleep(30)