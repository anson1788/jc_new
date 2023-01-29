#Simple assignment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import urllib.request
import os
import time
from datetime import datetime
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
    print("get btn")
    btn = driver.find_elements(by=By.CLASS_NAME,value='close')
time.sleep(1)
btn[0].click()


username = driver.find_elements(by=By.CLASS_NAME,value='username-btn')
while(len(username)==0):
    print("username")
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



url ='https://www.dc239.com/gamelobby/live'
time.sleep(1)
try:
    driver.get(url)
except Exception as e:
    print("keep")
submenu = driver.find_elements(by=By.CLASS_NAME,value='gp-logo')
while(len(submenu)==0):
    submenu = driver.find_elements(by=By.CLASS_NAME,value='gp-logo')

submenu[0].click()

Whandles = driver.window_handles
driver.switch_to.window(Whandles[1])
print(Whandles)
time.sleep(5)
driver.get(houseUrl)
time.sleep(2)

duration = 1  # seconds
freq = 440  # Hz
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

betDict = {}
while True:
    
    try:
        currentUrl = driver.current_url
    except Exception as e:
        print("block sll")
        diffInS = (datetime.now() - progStartTime).total_seconds()
        if diffInS > 5*60:
            os.system('sh rerungame.sh &')
        sys.exit()

    while currentUrl!=houseUrl:
        print("getHouseUrl")
        driver.get(houseUrl)
        time.sleep(2)
        currentUrl = driver.current_url

    try:
        diceRoadLi = driver.find_elements(by=By.ID,value='diceRoadLi')
        diceRoadTime = 0
        while(len(diceRoadLi)==0):
            print("geting diceRoad")
            diceRoadTime = diceRoadTime + 1
            diceRoadLi = driver.find_elements(by=By.ID,value='diceRoadLi')
            print("block here2")
            if diceRoadTime>200:
                diffInS = (datetime.now() - progStartTime).total_seconds()
                if diffInS > 5*60:
                    os.system('sh rerungame.sh &')
                sys.exit()
            else:
                print("block here")

        diceRoadLi[0].click()

        print("new loop")
        diceRoadPositionDiv = driver.find_elements(by=By.ID,value='diceRoadPositionDiv')
        diceRoadPositionDivCounter = 0
        while(len(diceRoadPositionDiv)==0):
            diceRoadPositionDivCounter = diceRoadPositionDivCounter + 1
            diceRoadPositionDiv = driver.find_elements(by=By.ID,value='diceRoadPositionDiv')
            if diceRoadPositionDivCounter > 200 :
                diffInS = (datetime.now() - progStartTime).total_seconds()
                if diffInS > 5*60:
                    os.system('sh rerungame.sh &')
                sys.exit()
        time.sleep(1)
        

        arr = []
        arr = diceRoadPositionDiv[0].find_elements(By.XPATH, "div")

  

        
        crtRound = driver.find_elements(by=By.ID,value='currentShoeRound')
        crtRoundTxt = crtRound[0].get_attribute('innerHTML').replace(" ", "")
        print(crtRoundTxt)
        resultList = list()
        resultListOE = list()
        resultListVal = list()
        idx = 0


        maxGame = 0
        gameList = {}
        for x in arr:
            eId = str(x.get_attribute('id'))
            eIdx = eId.split("_")
           
            col=int(eIdx[1])
            row=int(eIdx[2])
            idxGameIdx = 0 
            idxGameIdx = idxGameIdx + col*5 +  row + 1
            gameList[str(idxGameIdx)] = x
            maxGame = max(maxGame,idxGameIdx)

        reverseRow = (maxGame-1)%5
        reverseCol = (maxGame-1-reverseRow)/5
        reverseCol = int(reverseCol)
    
        for idxX in range(maxGame, maxGame-20, -1):
            x = gameList[str(idxX)]
            listp = x.find_elements(By.XPATH, "p")
            result = listp[0].get_attribute('innerHTML')
            #print(result[0] + "-"+result[1]+'-'+result[2])
            resultInt = int(result[0])+int(result[1])+int(result[2])
            putV = 'S'
            if int(resultInt)>10:
                putV = 'L'
            if result[0] == result[1] and result[1] == result[2]:
                putV = 'T'
            resultList.append(putV)
            valList = [result[0],result[1],result[2]]
            resultListVal.append(valList)
            if putV == 'T' :
                resultListOE.append("T")
            elif int(resultInt)%2 == 0:
                resultListOE.append("E")
            else :
                resultListOE.append("O")
 
        #bigSmallRoadLi = driver.find_elements(by=By.ID,value='bigSmallRoadLi')
        #bigSmallRoadLi[0].click()
        '''
        for x in arr:
            eId = x.get_attribute('id')
            eIdx = eId.split("_")
            if idx < 10:
                listp = x.find_elements(By.XPATH, "p")
                result = listp[0].get_attribute('innerHTML')
                print(result[0] + "-"+result[1]+'-'+result[2])
                resultInt = int(result[0])+int(result[1])+int(result[2])
                putV = 'S'
                if int(resultInt)>10:
                    putV = 'L'
                if result[0] == result[1] and result[1] == result[2]:
                    putV = 'T'
                resultList.append(putV)
                idx = idx + 1
            else :
                break
        '''
        Re = len(resultList)
        
        def playBet(betValue,maxGame):
            countdown = driver.find_elements(by=By.ID,value='countdown')
            countdownR = countdown[0].find_elements(By.XPATH, "span")
            countdownTxt = countdownR[0].get_attribute('innerHTML')
            if countdownTxt == "":
                return
            if str(maxGame) in betDict:
                return
            lastBet = 0 
            placeBet = 50
            if str(maxGame-1) in betDict:
                if betDict[str(maxGame-1)]["type"]==betValue:
                    lastBet = betDict[str(maxGame-1)]["bet"]
            if lastBet!=0:
                placeBet = lastBet*2
            #if placeBet>800:
                #placeBet = 800
            playSound()
            chips = driver.find_elements(by=By.ID,value='chips')
            
            chipsSet = chips[0].find_elements(By.XPATH, "li")
            if placeBet == 50:
                chipsSet[3].click()
            
            if placeBet == 100:
                chipsSet[4].click()

            if placeBet == 200 or placeBet == 400 or placeBet == 800 or placeBet == 1600:
                chipsSet[5].click()

            time.sleep(0.2)
            betName = ''
            if betValue == "SMALL":
                betName = 'BetSmall'
            if betValue == "BIG":
                betName = 'BetBig'
            if betValue == "EVEN":
                betName = 'BetEven'
            if betValue == "ODD":
                betName = 'BetOdd'
            if betValue == "ONE":
                betName = 'BetS1'
            if betValue == "TWO":
                betName = 'BetS2'
            if betValue == "THR":
                betName = 'BetS3'
            if betValue == "FOU":
                betName = 'BetS4'
            if betValue == "FIV":
                betName = 'BetS5'
            if betValue == "SIX":
                betName = 'BetS6'
            if betName !="":      
                btnIcon = driver.find_elements(by=By.ID,value=betName)
                btnIcon[0].click()
                if placeBet == 400:
                   time.sleep(0.2)
                   btnIcon[0].click()
                if placeBet == 800:
                   time.sleep(0.2)
                   btnIcon[0].click()
                   time.sleep(0.2)
                   btnIcon[0].click()
                   time.sleep(0.2)
                   btnIcon[0].click()
                if placeBet == 1600:
                   time.sleep(0.1)
                   btnIcon[0].click()
                   time.sleep(0.1)
                   btnIcon[0].click()
                   time.sleep(0.1)
                   btnIcon[0].click()
                   time.sleep(0.1)
                   btnIcon[0].click()
                   time.sleep(0.1)
                   btnIcon[0].click()
                   time.sleep(0.1)
                   btnIcon[0].click()
                   time.sleep(0.1)
                   btnIcon[0].click()

            time.sleep(0.2)
            confirm = driver.find_elements(by=By.ID,value='confirm')
            confirm[0].click()
            betDict[str(maxGame)]={}
            betDict[str(maxGame)]["bet"]=placeBet
            betDict[str(maxGame)]["type"]=betValue
        
        def checkVal(valIdx,checkVal):
            isMiss = True
            for y in range(valIdx):
                if resultListVal[y][0]==checkVal:
                   isMiss=False 
                if resultListVal[y][1]==checkVal:
                   isMiss=False 
                if resultListVal[y][2]==checkVal:
                   isMiss=False 
            return isMiss
        def checkIsHereValSingle(valIdx,checkVal):
            isHere = False
            if resultListVal[0][0]==checkVal:
                   isHere=True 
            if resultListVal[0][1]==checkVal:
                   isHere=True 
            if resultListVal[0][2]==checkVal:
                   isHere=True 
            return isHere

        seqIdx = 9
        seqValIdx = 9
        if Re>seqIdx:
            AllSmall=True 
            AllBig = True

            AllEven=True 
            AllOdd = True
            print('-----')
            for y in range(seqIdx):
                print(resultList[y])
            print('*******')
            for y in range(seqIdx):
                print(resultListOE[y])
            for y in range(seqIdx):
                if resultList[y]=='L':
                   AllSmall=False 
            for y in range(seqIdx):
                if resultList[y]=='S':
                   AllBig=False 
            for y in range(seqIdx):
                if resultListOE[y]=='E':
                   AllOdd=False 
            for y in range(seqIdx):
                if resultListOE[y]=='O':
                   AllEven=False 
            oneMissing = checkVal(seqValIdx,"1")
            twoMissing = checkVal(seqValIdx,"2")
            thrMissing = checkVal(seqValIdx,"3")
            fouMissing = checkVal(seqValIdx,"4")
            fivMissing = checkVal(seqValIdx,"5")
            sixMissing = checkVal(seqValIdx,"6")

            lastBetType = ""
            if str(maxGame-1) in betDict:
                lastBetType = betDict[str(maxGame-1)]["type"]
            if lastBetType != "":
                if lastBetType == "SMALL" and resultList[0]=='S':
                   lastBetType=""
                   betDict = {}
                elif lastBetType == "BIG"  and resultList[0]=='L':
                   lastBetType=""
                   betDict = {}
                elif lastBetType == "EVEN"  and resultListOE[0]=='E':
                   lastBetType=""
                   betDict = {}
                elif lastBetType == "ODD"  and resultListOE[0]=='O':
                   lastBetType=""
                   betDict = {}
                elif lastBetType == "ONE"  and checkIsHereValSingle(seqValIdx,"1"):
                   lastBetType=""
                   betDict = {}
                elif lastBetType == "TWO"  and checkIsHereValSingle(seqValIdx,"2"):
                   lastBetType=""
                   betDict = {}
                elif lastBetType == "THR"  and checkIsHereValSingle(seqValIdx,"3"):
                   lastBetType=""
                   betDict = {}
                elif lastBetType == "FOU"  and checkIsHereValSingle(seqValIdx,"4"):
                   lastBetType=""
                   betDict = {}
                elif lastBetType == "FIV"  and checkIsHereValSingle(seqValIdx,"5"):
                   lastBetType=""
                   betDict = {}
                elif lastBetType == "SIX"  and checkIsHereValSingle(seqValIdx,"6"):
                   lastBetType=""
                   betDict = {}


            if lastBetType == "":
                if AllBig == True:
                    playBet("SMALL",maxGame)
                elif AllSmall == True:
                    playBet("BIG",maxGame)
                elif AllOdd == True:
                    playBet("EVEN",maxGame)
                elif AllEven == True:
                    playBet("ODD",maxGame)
                elif oneMissing == True:
                    playBet("ONE",maxGame)
                elif twoMissing == True:
                    playBet("TWO",maxGame)
                elif thrMissing == True:
                    playBet("THR",maxGame)
                elif fouMissing == True:
                    playBet("FOU",maxGame)
                elif fivMissing == True:
                    playBet("FIV",maxGame)
                elif sixMissing == True:
                    playBet("SIX",maxGame)
                else :
                    betDict = {}
                    diffInS = (datetime.now() - progStartTime).total_seconds()
                    if diffInS > 25*60:
                        os.system('sh rerungame.sh &')
                        sys.exit()
            elif lastBetType=="SMALL" and AllBig == True:
                playBet("SMALL",maxGame)
            elif lastBetType=="BIG" and AllSmall == True:
                playBet("BIG",maxGame)
            elif lastBetType=="EVEN" and AllOdd == True:
                playBet("EVEN",maxGame)
            elif lastBetType=="ODD" and AllEven == True:
                playBet("ODD",maxGame)
            elif lastBetType=="ONE" and oneMissing == True:
                playBet("ONE",maxGame)
            elif lastBetType=="TWO" and twoMissing == True:
                playBet("TWO",maxGame)
            elif lastBetType=="THR" and thrMissing == True:
                playBet("THR",maxGame)
            elif lastBetType=="FOU" and fouMissing == True:
                playBet("FOU",maxGame)
            elif lastBetType=="FIV" and fivMissing == True:
                playBet("FIV",maxGame)
            elif lastBetType=="SIX" and sixMissing == True:
                playBet("SIX",maxGame)
        #playBet("ODD",maxGame)
            
        time.sleep(1)
    except Exception as e:
        print("exception "+ str(e))
        driver.get(houseUrl)
        time.sleep(2)