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
from IPython.display import clear_output
if tf.test.gpu_device_name():
    print('Default GPU Device Details: {}'.format(tf.test.gpu_device_name()))
    gpus = tf.config.list_physical_devices('GPU')
    try:
        tf.config.set_visible_devices(gpus[0], 'GPU')
        logical_gpus = tf.config.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPU")
    except RuntimeError as e:
        # Visible devices must be set before GPUs have been initialized
        print(e)
else:
    print("Please install Tensorflow that supports GPU")

'''
define model and data path
'''
platform = "mac"

mypath = "D:\\jc_new2\\excel"
modelpath = "D:\\jc_new2\\modelData"
if platform == "mac":
    mypath = "/Users/hello/jc_new2/excel"
    modelpath = "/Users/hello/jc_new2/modelData"

# start read data end 
files = listdir(mypath)
dataList = []
print("-----")
for f in files:
    fullpath = join(mypath, f)
    fileNameTime = f.replace(".xlsx", "")
    df = pd.read_excel(fullpath)
    dataList.append(df)
print(len(dataList))
print("-----")
# read data end 



import matplotlib.pyplot as plt

inputLength = 14
outputlength = 3

learningRate = 0.001
brain = Brain(inputLength, outputlength, learningRate)

env = cornerEnv(dataList)

maxMemory = 200
gamma = 0.8
DQN = Dqn(maxMemory, gamma)
#brain.model = keras.models.load_model(modelpath)
model = brain.model



batchSize = 5
epsilon = 1
epsilonDecayRate = 0.999


epoch = 0

currentState = np.zeros((1, inputLength))
nextState = currentState
totReward = 0
rewards = list()


while epoch<5000:
    epoch += 1
    currentState = [env.reset()]
    nextState = currentState.copy()
    gameOver = False
    oddListData = list()
    DQN.resetMemory()
    while not gameOver:

        if np.random.rand() <= epsilon:
            action = np.random.randint(0, 3)
        else:
            qvalues = model.predict(np.array([currentState[0]]))[0]
            action = np.argmax(qvalues)
        #print("action ",action)
        nextState[0], reward, gameOver, oddlist = env.step(action)
      
        totReward += reward

        DQN.remember([currentState[0], action, reward, nextState[0]], gameOver)
        inputs, targets = DQN.getBatch(model, batchSize)
        model.train_on_batch(inputs, targets)
          
        currentState = nextState
        if gameOver ==True:
            oddListData = oddlist
    if epoch%4==0:
        epsilon *= epsilonDecayRate
    if epoch%20==0: 
        for idx in range(len(oddListData)):
            print("odd ", oddListData[idx])
        #print("reward ", reward)
        print('Epoch: ' + str(epoch) + ' Epsilon: {:.5f}'.format(epsilon) + ' Total Reward: {:.2f}'.format(totReward))
        #print('odd',oddListData)
        model.save(modelpath)
    rewards.append(totReward)
    totReward = 0


plt.plot(rewards)
plt.xlabel('Epoch')
plt.ylabel('Rewards')
plt.show()
