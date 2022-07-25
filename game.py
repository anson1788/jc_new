#Simple assignment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
import sys
import urllib.request
import os
import time
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option("detach", True)

os.system('killall Google\ Chrome')


#driver = webdriver.Chrome(executable_path='C:\Windows\chromedriver.exe',options=chrome_options)
driver = webdriver.Chrome(executable_path='/Users/hello/Desktop/chrome/chromedriver',options=chrome_options)


houseUrl = "https://bpweb.fuximex555.com/player/singleSicTable.jsp?dm=1&t=51&title=1&sgt=4&hall=1&mute=1"
#houseUrl = "https://bpweb.fuximex555.com/player/singleSicTable.jsp?dm=1&t=551&title=1&sgt=4&hall=4&mute=1"



def playSound():
  os.system('afplay sound/bet.wav &')

playSound()


loopIdx = 0
url ='https://www.dc239.com'
driver.get(url)
btn = driver.find_elements(by=By.CLASS_NAME,value='mps-close')
while(len(btn)!=1):
    btn = driver.find_elements(by=By.CLASS_NAME,value='mps-close')
btn[0].click()


username = driver.find_elements(by=By.CLASS_NAME,value='username-btn')
while(len(username)!=1):
    username = driver.find_elements(by=By.CLASS_NAME,value='username-btn')
username[0].send_keys("anson1788")

password = driver.find_elements(by=By.CLASS_NAME,value='password-btn')
while(len(password)!=1):
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
driver.get(url)
submenu = driver.find_elements(by=By.CLASS_NAME,value='gp-logo')
print(submenu)
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
    
    currentUrl = driver.current_url
    while currentUrl!=houseUrl:
        print("getHouseUrl")
        driver.get(houseUrl)
        time.sleep(2)
        currentUrl = driver.current_url

    try:
        diceRoadLi = driver.find_elements(by=By.ID,value='diceRoadLi')
        print(diceRoadLi)
        while(len(diceRoadLi)==0):
            diceRoadLi = driver.find_elements(by=By.ID,value='diceRoadLi')
        print("----")
        print(diceRoadLi)
        diceRoadLi[0].click()

            
        diceRoadPositionDiv = driver.find_elements(by=By.ID,value='diceRoadPositionDiv')
        while(len(diceRoadPositionDiv)==0):
            diceRoadPositionDiv = driver.find_elements(by=By.ID,value='diceRoadPositionDiv')
        time.sleep(1)
        arr = diceRoadPositionDiv[0].find_elements(By.XPATH, "div")

  

        
        crtRound = driver.find_elements(by=By.ID,value='currentShoeRound')
        crtRoundTxt = crtRound[0].get_attribute('innerHTML').replace(" ", "")
        print(crtRoundTxt)
        resultList = list()
        idx = 0
        for x in arr:
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
        Re = len(resultList)
        
        def playBet(betValue,gameRound):
            playSound()
            if betDict.has_key(betValue):
                return
            playSound()
            chips = driver.find_elements(by=By.ID,value='chips')
            chipsSet = chips[0].find_elements(By.XPATH, "li")
            chipsSet[3].click()
            if betValue == "SMALL":
                small = driver.find_elements(by=By.ID,value='BetSmall')
                small[0].click()
            if betValue == "BIG":
                big = driver.find_elements(by=By.ID,value='BetBig')
                big[0].click()
            time.sleep(1)
            confirm = driver.find_elements(by=By.ID,value='confirm')
            #confirm[0].click()
            betDict[gameRound]={}
            betDict[gameRound]["bet"]=betValue
        
        if Re>5:
            AllSmall=True 
            AllBig = True
            print('-----')
            for y in range(5):
                print(resultList[y])
            for y in range(5):
                if resultList[y]!='S':
                   AllSmall=False 
            for y in range(5):
                if resultList[y]!='L':
                   AllBig=False 
            if AllBig == True:
                playBet("BIG",crtRoundTxt)
            if AllSmall == True:
                playBet("SMALL",crtRoundTxt)

            
        time.sleep(1)
    except:
        print("exception")
        driver.get(houseUrl)
        time.sleep(2)