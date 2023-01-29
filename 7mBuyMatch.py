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
import traceback

os.system('pkill -f firefox')


#driver = webdriver.Chrome(executable_path='C:\Windows\chromedriver.exe',options=chrome_options)
driver = webdriver.Firefox(executable_path='/Users/hello/Desktop/chrome/geckodriver')


def loadPage(url):
    loopIdx = 0
    driver.set_page_load_timeout(10)
    try:
        driver.get(url)
        time.sleep(1)
    except Exception as e:
        print("keep")

def login():
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

def startBetPage():
    submenu = driver.find_elements(by=By.CLASS_NAME,value='btn-main')
    while(len(submenu)==0):
        submenu = driver.find_elements(by=By.CLASS_NAME,value='btn-main')
    submenu[3].click()  

def switchWindow():
    Whandles = driver.window_handles
    driver.switch_to.window(Whandles[1])
    time.sleep(5)
    print(Whandles)

def switchLang():
   #print(driver.current_url.replace("lang=EN","lang=zh-cn"))
   loadPage(driver.current_url.replace("lang=EN","lang=zh-cn"))

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def removeSpace(StringInput):
    StringInput = StringInput.strip().replace(" ","")
    pattern = re.compile(r'\s+')
    StringInput = re.sub(pattern, '', StringInput)
    return StringInput
def scanGameList():
    screenData = driver.find_element(By.XPATH, '//*[@id="odds-display-live"]')
    tbody = screenData.find_elements(By.TAG_NAME,"tbody")
    for idx,x in enumerate(tbody) :
        trs = x.find_elements(By.TAG_NAME,"tr")
        if len(trs) == 3:
            for idy,y in enumerate(trs) :
                if idy == 0:
                    tds = y.find_elements(By.TAG_NAME,"td")
                    #print(remove_html_tags(tds[2].get_attribute("innerHTML")).strip().replace(" ",""))
                    matchCrt = tds[0].find_element(By.XPATH,".//*[@class='time-column-content']")
                    #matchCrt.find_element(By.XPATH,"//*[@class='score ']")
                    scoreString = matchCrt.find_element(By.XPATH,".//*[@class='score ']").get_attribute("innerHTML").strip().replace(" ","")
                    scoreString = remove_html_tags(scoreString).strip().replace(" ","")
                    scoreString = removeSpace(scoreString)
                    statusString = matchCrt.find_element(By.XPATH,".//*[@class='Red']").get_attribute("innerHTML").strip().replace(" ","")
                    statusString = statusString.split("'")[0]
                    if '半场' in statusString:
                        statusString = ""

                    homeTeam = ""
                    awayTeam = ""
                    spanArr = tds[2].find_elements(By.TAG_NAME,"span")
                    homeTeam = removeSpace(spanArr[1].get_attribute("innerHTML")).split("(")[0]
                    awayTeam = removeSpace(spanArr[2].get_attribute("innerHTML")).split("(")[0]
                    if '1H' in statusString:
                        print(scoreString)
                        print(statusString)
                        print(homeTeam , " vs " ,awayTeam)    
                        oddPoint = ""
                        oddRatio = ""
                        if len(tds[8].find_elements(By.XPATH,".//*[@class='hdp-point']"))>0:
                            oddPoint = tds[8].find_element(By.XPATH,".//*[@class='hdp-point']").get_attribute("innerHTML")
                        if len(tds[8].find_elements(By.XPATH,".//*[@class='odds black']"))>0:
                            oddRatio = tds[8].find_element(By.XPATH,".//*[@class='odds black']").get_attribute("innerHTML")
                        print(oddPoint , " " , oddRatio)

                        if homeTeam == '艾华迪堡':
                            #*[@id="bu:od:price:1168346490:h:0.70:1"]
                            tds[8].find_element(By.XPATH,".//*[@class='odds black']").click()
                        print("----")  
                       
                    '''
                    for idz,z in enumerate(tds) :
                        print(remove_html_tags(z.get_attribute("innerHTML")).replace(" ",""))
                        print("----")
                    '''
        
                        

'''start the program'''   
loadPage('https://www.dc239.com')
login()
loadPage('https://www.dc239.com/gamelobby/sports')
startBetPage()
switchWindow()
switchLang()
scanGameList()