def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import gym
import json
import datetime as dt
from env.cornerEnv import cornerEnv
from os import listdir
from os.path import isfile, isdir, join
import pandas as pd
import numpy as np
from brain import Brain
from dqn import Dqn
import tensorflow as tf
from tensorflow import keras
if tf.test.gpu_device_name():
    print('Default GPU Device Details: {}'.format(tf.test.gpu_device_name()))
else:
    print("Please install Tensorflow that supports GPU")
    
mypath = "D:\\jc_new\\excel"
modelpath = "D:\\jc_new\\model2604"
#mypath = "/Users/hello/jc_new/excel"

files = listdir(mypath)


dataList = []
for f in files:
    fullpath = join(mypath, f)
    fileNameTime = f.replace(".xlsx", "")
    df = pd.read_excel(fullpath)
    dataList.append(df)

#env = cornerEnv(dataList)
#env.reset()


#verify step
'''
for idx in range(30):
    state, reward , done, _ = env.step(0)
    #print(idx)
    print(reward)
    if done == True:
        break
'''


import matplotlib.pyplot as plt
learningRate = 0.001
maxMemory = 50000
gamma = 0.9
batchSize = 10
epsilon = 1.
epsilonDecayRate = 0.995

env = cornerEnv(dataList)
brain = Brain(5, 3, learningRate)
brain.model = keras.models.load_model(modelpath)
model = brain.model
DQN = Dqn(maxMemory, gamma)

epoch = 0
currentState = np.zeros((1, 5))
nextState = currentState
totReward = 0
rewards = list()


currentState = [env.reset()]
nextState = currentState.copy()
oddListData = list()
gameOver = False
while not gameOver:
    qvalues = model.predict(np.array([currentState[0]]))[0]
    action = np.argmax(qvalues)
    nextState[0], reward, gameOver, oddList = env.stepTrue(action)
    currentState = nextState
    if gameOver == True:
        oddListData = oddList
        totReward = reward
    

print("odd ", oddListData)
print("reward ", reward)