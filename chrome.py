#Simple assignment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time
import MySQLdb
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
#driver = webdriver.Chrome(executable_path='C:\Windows\chromedriver.exe',options=chrome_options)
driver = webdriver.Chrome(executable_path='C:\Windows\chromedriver.exe',options=chrome_options)

loopIdx = 0
url ='https://bet.hkjc.com/football/odds/odds_chl.aspx?lang=ch'
driver.get(url)
time.sleep(5)
datas = driver.find_elements(by=By.CLASS_NAME,value='couponTable')
for data in datas:
    header=data.find_elements(by=By.CLASS_NAME,value="tgCoupon")
    obj=data.find_elements(by=By.CLASS_NAME, value=header[0].get_attribute("id"))
    for singleMatch in obj:
        inplay = singleMatch.find_elements(by=By.CLASS_NAME,value='inplayLnkInRow')
        inplaylen = len(inplay)
        if inplaylen > 0:
            alloddsLink = inplay[0].find_elements(by=By.CLASS_NAME,value='alloddsLink')
            alloddsLinklen = len(alloddsLink)
            if alloddsLinklen > 0:
                loopIdx = loopIdx + 1

print(loopIdx)



pointer = 0
def getUrl(idx):
    url ='https://bet.hkjc.com/football/odds/odds_chl.aspx?lang=ch'
    driver.get(url)
    datas = driver.find_elements(by=By.CLASS_NAME,value='couponTable')
    for x in range(len(datas)):
        data=datas[x]
        header=data.find_elements(by=By.CLASS_NAME,value="tgCoupon")
        obj=data.find_elements(by=By.CLASS_NAME, value=header[0].get_attribute("id"))
        for y in range(len(obj)):    
            singleMatch = obj[y]
            if idx==y :
                inplay = singleMatch.find_elements(by=By.CLASS_NAME,value='inplayLnkInRow')
                inplaylen = len(inplay)
                if inplaylen > 0:
                    alloddsLink = inplay[0].find_elements(by=By.CLASS_NAME,value='alloddsLink')
                    alloddsLinklen = len(alloddsLink)
                    if alloddsLinklen > 0:
                        alloddsLink[0].click()
                        time.sleep(1)
                        print("---")
                        time.sleep(1)
                        print("---")
                        time.sleep(1)
                        print("---")
                        time.sleep(1)
                        print("---")
                        time.sleep(1)
                        print("---")
                        print("---")
                        get_url = driver.current_url
                        print(get_url)
                        return get_url

#for x in range(loopIdx):
    #getUrl(x)
driver.close()



def doQuery( conn ) :
    cur = conn.cursor()
    cur.execute( "SELECT * FROM matchTable" )
    for firstname, lastname in cur.fetchall() :
        print( firstname, lastname )

hostname = '47.243.95.214'
username = 'r1'
password = 'Ra123456!'
database = 'hkjc'

print( "Using mysqlclient (MySQLdb):" )
import MySQLdb
myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database,port=3306 )
doQuery( myConnection )
myConnection.close()