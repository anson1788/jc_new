from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
import sys
import  time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from blackJackCloud import getChromeDriverPath

import pyautogui
"""Sample prediction script for TensorFlow 2.x."""
import sys
import tensorflow as tf
import numpy as np
from PIL import Image
from object_detection import ObjectDetection
import time

MODEL_FILENAME = 'model/model.pb'
LABELS_FILENAME = 'model/labels.txt'


class TFObjectDetection(ObjectDetection):
    """Object Detection class for TensorFlow"""

    def __init__(self, graph_def, labels):
        super(TFObjectDetection, self).__init__(labels)
        self.graph = tf.compat.v1.Graph()
        with self.graph.as_default():
            input_data = tf.compat.v1.placeholder(tf.float32, [1, None, None, 3], name='Placeholder')
            tf.import_graph_def(graph_def, input_map={"Placeholder:0": input_data}, name="")

    def predict(self, preprocessed_image):
        inputs = np.array(preprocessed_image, dtype=float)[:, :, (2, 1, 0)]  # RGB -> BGR

        with tf.compat.v1.Session(graph=self.graph) as sess:
            output_tensor = sess.graph.get_tensor_by_name('model_outputs:0')
            outputs = sess.run(output_tensor, {'Placeholder:0': inputs[np.newaxis, ...]})
            return outputs[0]


def main(image_filename):
    # Load a TensorFlow model
    graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(MODEL_FILENAME, 'rb') as f:
        graph_def.ParseFromString(f.read())

    # Load labels
    with open(LABELS_FILENAME, 'r') as f:
        labels = [label.strip() for label in f.readlines()]

    od_model = TFObjectDetection(graph_def, labels)

    image = Image.open(image_filename)
    predictions = od_model.predict_image(image)
    #print(predictions)
    for x in predictions:
        if x["probability"] >0.35:
            print(predictions)
            return




options = ChromeOptions()
chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()
chrm_caps['goog:loggingPrefs'] = { 'performance':'ALL' }

options.debugger_address = "127.0.0.1:" + '9222'
browser = webdriver.Chrome(service=Service(executable_path=getChromeDriverPath()), options=options,desired_capabilities=chrm_caps)
#browser.get("https://evo.nomisma88.com/frontend/evo/r2/#category=all_games&game=blackjack&table_id=sni5cza6d1vvl50i&lobby_launch_id=1756b3d19e574cb2b9cfb74537dd8f0b")

import os
import json
import cv2
import numpy as np


lastCallTime = 0
def countValue(cardIx):

    return 0

def saveGameState(str):
    res = json.dumps(str,ensure_ascii=False, indent=4)
    with open("bjGame/gameStatus.json", "w",encoding="utf8") as outfile:
        outfile.write(res)

def saveGameCard(str):
    temp = []
    result = dict()
    for key, val in str.items():
        result[key] = val
    res = json.dumps(result,ensure_ascii=False, indent=4)
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


def playSound(lastCallTime):
  curr_time = round(time.time()*1000)
  print(curr_time)
  print(lastCallTime)
  if(curr_time-lastCallTime > 10000):
    os.system('afplay sound/bet.wav &')
    return curr_time
  return lastCallTime

def calEV():
    cardlocalArr = {}
    totalEV = 0
    with open("bjGame/cardArr.json") as json_file:
        cardlocalArr = json.load(json_file)
    #print(cardlocalArr)
    for x in cardlocalArr:
        val = '-1'
        val = cardlocalArr[x][0]
        if val == '2':  
            totalEV = totalEV + 5
        elif val == '3':
            totalEV = totalEV + 6
        elif val == '4':
            totalEV = totalEV + 8
        elif val == '5':
            totalEV = totalEV + 11  
        elif val == '6':
            totalEV = totalEV + 6  
        elif val == '7':
            totalEV = totalEV + 4    
        elif val == '9':
            totalEV = totalEV - 3  
        elif val == 'A':
            totalEV = totalEV - 9 
        elif(
            val == 'T' or 
            val == 'J' or 
            val == 'Q' or 
            val == 'K' 
        ):
            totalEV = totalEV - 7    
        '''
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
        '''
    trueEV = 0
    if len(cardlocalArr)==0:
        trueEV = 0
    else:
        trueEV = totalEV / ((52*8 - len(cardlocalArr))/52)
    return trueEV

def checkScreen(counterIdx):
    isRedCardFound = False
    if counterIdx % 5 == 0 and counterIdx != 0:
        counterIdx = 0
    return counterIdx,isRedCardFound

def checkGameActive():
    try:
        backCard = browser.find_elements(by=By.TAG_NAME,value="div")
        for div in backCard:
            attr = div.get_attribute("data-role")
            if attr == "inactivity-message-clickable":
                print (attr)
                div.click()
                print("found black")
    except Exception as e:
        a = 1


gameStatus = {}
cardMastArr = {}
with open("bjGame/cardArr.json") as json_file:
    cardMastArr = json.load(json_file)


counterIdx = 0
isRedCardShowGlb = False

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1
pyautogui.size()
width, height = pyautogui.size()

print("Start game")
#y =  pyautogui.locateCenterOnScreen("bjGame/msg.png", grayscale=False, confidence = 0.5)
#print(y)
print("end game")

gameId = ""
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
    #checkGameActive()

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
                
                '''
                if (
                    json_object != None and "type" in json_object
                ):
                    print(json_object["type"])
                '''

                trueEV = calEV()
                if (
                    json_object != None and "type" in json_object and 
                    json_object["type"]=="blackjack.v3.chips"):
                    print("game : ", gameId," EV:", trueEV)
                    if trueEV > 1:
                        lastCallTime =  playSound(lastCallTime)
               
                if (
                    json_object != None and "eventType" in json_object and 
                    json_object["eventType"]=="PONG"
                ):
                    a=1
                elif json_object != None :
                    b=1
                    #print("---")
                    #print(json_object)
                if (
                    json_object != None and "type" in json_object and 
                    (json_object["type"]=="blackjack.v3.phase" or json_object["type"]=="blackjack.v3.game")
                ):
                    dealerCardArr = getDealerCard(json_object)
                    ''' [{'value': 'JS', 'deck': 5, 't': 1674235034766}]'''
                    for card in dealerCardArr:
                        if card['value']!='**':
                            key = str(card['value'])+str(card['deck'])+""
                            if key not in cardMastArr:
                                print("--dealer--")
                                print(key)
                                print(len(cardMastArr))
                                cardMastArr[key] = card['value']
                                print(len(cardMastArr))

                    seatArr = getSeatCard(json_object)
                    for card in seatArr:
                        if card['value']!='**':
                            key = str(card['value'])+str(card['deck'])+""
                            if key not in cardMastArr:
                                print("--normal--")
                                print(key)
                                print(len(cardMastArr))
                                cardMastArr[key] = card['value']
                                print(len(cardMastArr))
                            #print("add new card " + cardMastArr[card['t']])
                    saveGameCard(cardMastArr) 

                if len(wsJson["message"]["params"]["response"]["payloadData"])<500:
                    if "scalable.blackjack." in wsJson["message"]["params"]["response"]["payloadData"] and 'scalable.blackjack.statistics' not in wsJson["message"]["params"]["response"]["payloadData"]:
                        print(wsJson["message"]["params"]["response"]["payloadData"])
    counterIdx = counterIdx + 1
    screenResult = checkScreen(counterIdx)
    counterIdx = screenResult[0]
    isRedCardShow = screenResult[1]

