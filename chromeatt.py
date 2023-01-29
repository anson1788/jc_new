from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
import sys
import  time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
options = ChromeOptions()
chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()
chrm_caps['goog:loggingPrefs'] = { 'performance':'ALL' }

options.debugger_address = "127.0.0.1:" + '9222'
browser = webdriver.Chrome(service=Service(executable_path="/Users/hello/Desktop/chrome/chromedriver109"), options=options,desired_capabilities=chrm_caps)
#browser.get("https://evo.nomisma88.com/frontend/evo/r2/#category=all_games&game=blackjack&table_id=sni5cza6d1vvl50i&lobby_launch_id=1756b3d19e574cb2b9cfb74537dd8f0b")

import os
import json

def countValue(cardIx):

    return 0

def saveGameState(str):
    res = json.dumps(str,ensure_ascii=False, indent=4)
    with open("bjGame/gameStatus.json", "w",encoding="utf8") as outfile:
        outfile.write(res)

def saveGameCard(str):
    res = json.dumps(str,ensure_ascii=False, indent=4)
    with open("bjGame/cardArr.json", "w",encoding="utf8") as outfile:
        outfile.write(res)

def getDealerCard(json_object):
    if (
         "args" in json_object and 
         "dealer" in json_object["args"] and 
         "cards" in json_object["args"]["dealer"]
    ):
        return json_object["args"]["dealer"]["cards"]
    else:
        return []

def getSeatCard(json_object):
    if (
         "args" in json_object and 
         "seats" in json_object["args"]
    ):  
        returnVal = []
        for x in json_object["args"]["seats"]:
            if "first" in json_object["args"]["seats"][x]:
                listArr = json_object["args"]["seats"][x]["first"]["cards"]
                for k in listArr:
                    returnVal.append(k)
            if "second" in json_object["args"]["seats"][x]:
                listArr = json_object["args"]["seats"][x]["second"]["cards"]
                for k in listArr:
                    returnVal.append(k)
        return returnVal
    else:
        return []

def calEV():
    cardlocalArr = {}
    totalEV = 0
    with open("bjGame/cardArr.json") as json_file:
        cardlocalArr = json.load(json_file)
    #print(cardlocalArr)
    for x in cardlocalArr:
        val = '-1'
        val = cardlocalArr[x][0]
        if (
            val == '2' or 
            val == '3' or 
            val == '4' or 
            val == '5' or 
            val == '6' 
        ):  
            totalEV = totalEV + 1
        elif(
            val == 'T' or 
            val == 'J' or 
            val == 'Q' or 
            val == 'K' or 
            val == 'A'
        ):
            totalEV = totalEV - 1
    trueEV = 0
    if len(cardlocalArr)==0:
        trueEV = 0
    else:
        trueEV = totalEV / ((52*8 - len(cardlocalArr))/52)
    return trueEV


gameStatus = {}
cardMastArr = {}
with open("bjGame/cardArr.json") as json_file:
    cardMastArr = json.load(json_file)

counterIdx = 0
while True:
    with open("bjGame/gameStatus.json") as json_file:
        gameStatus = json.load(json_file)
    if gameStatus["startCourt"] == '1':
        gameStatus["startCourt"] = '2'
        gameStatus["ev"] = 0
        cardMastArr = {}
        saveGameCard(cardMastArr)
        saveGameState(gameStatus)

    currentGame = {"phase":"pending"}
    for wsData in browser.get_log('performance'):
            wsJson = json.loads((wsData['message']))
            #element =browser.find_elements(By.TAG_NAME, 'input')[0].click()
            if wsJson["message"]["method"]== "Network.webSocketFrameReceived":
                dataStr = wsJson["message"]["params"]["response"]["payloadData"]
                json_object = None
                try:
                    json_object = json.loads(dataStr)
                except:
                    json_object = None
                if (
                    json_object != None and "type" in json_object and 
                    (json_object["type"]=="blackjack.v3.phase" or json_object["type"]=="blackjack.v3.game")
                ):
                    dealerCardArr = getDealerCard(json_object)
                    ''' [{'value': 'JS', 'deck': 5, 't': 1674235034766}]'''
                    for card in dealerCardArr:
                        if card['t'] not in cardMastArr and card['value']!='**':
                            cardMastArr[card['t']] = card['value']
                            print("add new card " + cardMastArr[card['t']])

                    seatArr = getSeatCard(json_object)
                    for card in seatArr:
                        if card['t'] not in cardMastArr and card['value']!='**':
                            cardMastArr[card['t']] = card['value']
                            print("add new card " + cardMastArr[card['t']])
                    saveGameCard(cardMastArr) 
                    trueEV = calEV()
                    counterIdx = counterIdx + 1
                    if counterIdx % 5 == 0 and counterIdx != 0:
                        #browser.save_screenshot("bjGame/image.png")
                        counterIdx = 0
                    print("print trueEV : ", trueEV)
                    
                '''
                    if json_object["type"]=="blackjack.v3.phase" and json_object["args"]["name"]=="InitialDealing":
                        currentGame = {"phase":"start"}
                    if json_object["type"]=="blackjack.v3.game" and currentGame["phase"]=="start":
                        currentGame["phase"] = "gameDealer"
                        currentGame["dealer"]= {"cards":{},"score":0}
                        currentGame["player"]= {}    
                    if dealer in currentGame:
                        currentGame["dealer"]["score"] = json_object["args"]["dealer"]["score"]
                        cardArr = json_object["args"]["dealer"]["cards"]
                        for card in cardArr:
                            if card["t"] not in currentGame["dealer"]["cards"]:
                                currentGame["dealer"]["cards"][card["t"]]=card["value"]
                    with open("example.txt", "a") as f:
                        f.write(str(json_object))
                        f.write("\n-----\n")

                '''


                if len(wsJson["message"]["params"]["response"]["payloadData"])<500:
                    if "scalable.blackjack." in wsJson["message"]["params"]["response"]["payloadData"] and 'scalable.blackjack.statistics' not in wsJson["message"]["params"]["response"]["payloadData"]:
                        print(wsJson["message"]["params"]["response"]["payloadData"])
                        #with open("example.txt", "w") as f:
                             #f.write(wsJson["message"]["params"]["response"]["payloadData"])
                #print ("Rx :"+ str(wsJson["message"]["params"]["timestamp"]) + wsJson["message"]["params"]["response"]["payloadData"])
                #print(wsJson["message"])
    time.sleep(1)
