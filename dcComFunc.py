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

progStartTime = datetime.now()

pageListUrl = ""
def playSound():
  os.system('afplay sound/bet.wav &')

#playSound()

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def getListData():
    screenData = driver.find_elements(By.XPATH, '//*[@id="Table3"]/tbody/tr')
    while True:
        screenData = driver.find_elements(By.XPATH, '//*[@id="Table3"]/tbody/tr')
        if(len(screenData) >2):
            break
    return screenData

def merge_two_dicts(x, y):
    """Given two dictionaries, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def getDetailsData(element):
    singelMatch = {}
    singelMatch["round"] = element[0].get_attribute("innerHTML")
    singelMatch["matchTime"] = element[1].get_attribute("innerHTML").replace("<br>", " ")
    #print(int(singelMatch["matchTime"].split(" ")[0].split("-")[0]))
    monthVal = int(singelMatch["matchTime"].split(" ")[0].split("-")[0])

    if int(str(date.today().month)) < monthVal:
        singelMatch["matchTime"] = str(int(date.today().year)-1) + "-"+ singelMatch["matchTime"]
    else:
        singelMatch["matchTime"] = str(date.today().year) + "-"+ singelMatch["matchTime"]

    homeNameInnerHtml = element[2].get_attribute("innerHTML")
    if len(element[2].get_attribute("innerHTML").split("</span>"))>1:
        homeNameInnerHtml = element[2].get_attribute("innerHTML").split("</span>")[1]
    awayNameInnerHtml = element[4].get_attribute("innerHTML")
    if len(element[4].get_attribute("innerHTML").split("</span>"))>1:
        awayNameInnerHtml = element[4].get_attribute("innerHTML").split("</span>")[1]
            
    singelMatch["home"] = remove_html_tags(homeNameInnerHtml).split("[")[0]
    singelMatch["away"] = remove_html_tags(awayNameInnerHtml).split("[")[0]
    singelMatch["Handicap"] = {
        "home":remove_html_tags(element[5].get_attribute("innerHTML")),
        "odd":remove_html_tags(element[6].get_attribute("innerHTML")),
        "away":remove_html_tags(element[7].get_attribute("innerHTML")),
    }
    singelMatch["result"] = remove_html_tags(element[3].get_attribute("innerHTML"))
    singelMatch["halfresult"] = remove_html_tags(element[9].get_attribute("innerHTML"))
    return singelMatch

def getOU(element):
    singelMatch = {}
    singelMatch["OU"] = {
        "home":remove_html_tags(element[5].get_attribute("innerHTML")),
        "odd":remove_html_tags(element[6].get_attribute("innerHTML")),
        "away":remove_html_tags(element[7].get_attribute("innerHTML")),
    }
    singelMatch["halfresult"] = remove_html_tags(element[9].get_attribute("innerHTML"))
    return singelMatch

def loadPage():
    loopIdx = 0
    print(pageListUrl)
    url = pageListUrl
    driver.set_page_load_timeout(10)
    try:
        driver.get(url)
        time.sleep(1)
    except Exception as e:
        print("keep")



def getPageData():
    #driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div[3]/div[2]/table/tbody/tr[1]/td[6]/select/option[1]').click()
    contentData = driver.find_elements(By.XPATH, "//div[@class='data']")[0]
    #listdata = contentData.find_elements(By.XPATH, "//div[@class='tdsolid']")[1]
    matchData = contentData.find_elements(By.XPATH, "//table[@id='Table3']")[0]

    screenData = getListData()

    for idx, x in enumerate(screenData):
        if idx != 0:
            tdList = x.find_elements(By.TAG_NAME, "td")
            matchID = x.get_attribute("id")
            singleMatch = getDetailsData(tdList)
            matchArr[matchID]=singleMatch


    btn = driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[3]/div[3]/table/tbody/tr[1]/td[6]/div/strong/div/span[2]/input')
    if(len(btn)==0):
       btn = driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[3]/div[2]/table/tbody/tr[1]/td[6]/div/strong/div/span[2]/input')
    btn[0].click() 
    screenData = getListData()
    for idx, x in enumerate(screenData):
        if idx != 0:
            tdList = x.find_elements(By.TAG_NAME, "td")
            matchID = x.get_attribute("id")
            OU = getOU(tdList)
            matchArr[matchID] = merge_two_dicts(OU,matchArr[matchID])
            #print(matchArr[matchID])




def runIdx(crtIdx):
    loadPage()                                
    listTr=driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[3]/table/tbody/tr/td/table/tbody/tr')
    if len(listTr) < 1:
        listTr=driver.find_elements(By.XPATH,' /html/body/div[4]/div[2]/div[3]/table/tbody/tr/td/div/table/tbody/tr')
    
    tdListARR = []
    for idx, x in enumerate(listTr):
        tdList = x.find_elements(By.TAG_NAME, "td")
        print(idx, " ", len(tdList))
        for idy, y in enumerate(tdList):
            if x == 0 and idy!=0:
                tdListARR.append(y)
            else:
                tdListARR.append(y)

    tdListARR.reverse()
    print("tdlist ",len(tdListARR))
    reverseLoopCount = 0 
    for idx, x in enumerate(tdListARR):
        if 'graybg' not in x.get_attribute("class"):
            if reverseLoopCount == crtIdx:
                if crtIdx != 0 :
                    x.click()
                print("trigger get page data with idx",crtIdx)
                getPageData()
            reverseLoopCount = reverseLoopCount + 1
    return reverseLoopCount-1

matchArr = {}

def tryAgain(x, retries=0):
    if retries > 10: return -1
    try:
        idx = runIdx(x)
        return idx , matchArr
    except:
        traceback.print_exc()
        retries+=1
        #return 0
        return tryAgain(x, retries)