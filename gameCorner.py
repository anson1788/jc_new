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
url ='https://www.dszuqiu.com/team/5983'
driver.set_page_load_timeout(10)
try:
    driver.get(url)
except Exception as e:
    print("keep")
time.sleep(2)

tag = driver.find_elements(By.TAG_NAME,"section")

teamName = driver.find_elements(By.TAG_NAME,"h1")
name = teamName[0].get_attribute("innerHTML").split(" / ")
print(name[0])
for idx, x in enumerate(tag):
    tagNameId = x.get_attribute("id")
    if(tagNameId=="ended"):
        tbody = x.find_elements(By.TAG_NAME,"tbody")
        tr = tbody[0].find_elements(By.TAG_NAME,"tr")
        for y in tr:
            tds = y.find_elements(By.TAG_NAME,"td")
            matchDate = ""
            homeName = ""
            homeGoal = ""
            homeGoalHalf = ""
            homeCorner = ""
            homeCornerHalf = ""
            awayName = ""
            awayGoal = ""
            awayGoalHalf = ""
            awayCorner = ""
            awayCornerHalf = ""
            for idx, x in enumerate(tds):
                #home team
                if idx == 2:
                    matchDate = x.text              
                if idx == 3:
                    homeName = x.find_elements(By.TAG_NAME,"a")[0].text.strip().replace(" ", "")
                #end result
                if idx == 4:
                    #print(idx, x)
                    homeGoal = x.text.split(" : ")[0]
                    awayGoal = x.text.split(" : ")[1]
                #end result
                if idx == 5:
                    awayName = x.find_elements(By.TAG_NAME,"a")[0].text.strip().replace(" ", "")
                if idx == 6:
                    homeGoalHalf = x.text.split(":")[0].strip().replace(" ", "")
                    awayGoalHalf = x.text.split(":")[1].strip().replace(" ", "")                  
                    #print(awayName[0].text)
                if idx == 9:
                    homeCornerHalf= x.text.split(":")[0].strip().replace(" ", "")
                    awayCornerHalf = x.text.split(":")[1].strip().replace(" ", "")                      
                if idx == 8:
                    #race_timeLine
                    details =  x.find_elements(By.ID,"race_timeLine")   
                    a = details[0].find_elements(By.TAG_NAME,"span")
                    for idy,y in enumerate(a):
                        if y.get_attribute("title")!="":
                            print(y.get_attribute("title"))
                    
                if idx == 10:
                    homeCorner = x.text.split(" : ")[0]
                    awayCorner = x.text.split(" : ")[1]                  
                    #print(awayName[0].text)
            print(homeName + " " + awayName + " - "+ homeGoal + " "+awayGoal + " | "+ homeGoalHalf + " "+awayGoalHalf)
            print(matchDate+" "+ homeCorner + " "+awayCorner + "|" +homeCornerHalf + " "+awayCornerHalf )
                
                #print( "---" )