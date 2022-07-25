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
    
#mypath = "D:\\jc_new\\excel"
#modelpath = "D:\\jc_new\\model2804"
mypath = "/Users/hello/jc_new/excel"

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
epsilon = 1
epsilonDecayRate = 0.995

env = cornerEnv(dataList)
brain = Brain(5, 3, learningRate)
#brain.model = keras.models.load_model(modelpath)
model = brain.model
DQN = Dqn(maxMemory, gamma)

epoch = 0
currentState = np.zeros((1, 5))
nextState = currentState
totReward = 0
rewards = list()


while epoch<2000:
    epoch += 1
    currentState = [env.reset()]
    nextState = currentState.copy()
    gameOver = False
    oddListData = list()
    '''
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
     
    for idx in range(len(oddListData)):
        print("odd ", oddListData[idx])
    #print("reward ", reward)
    print('Epoch: ' + str(epoch) + ' Epsilon: {:.5f}'.format(epsilon) + ' Total Reward: {:.2f}'.format(totReward))
    #print('odd',oddListData)
    model.save(modelpath)
    rewards.append(totReward)
    totReward = 0
    '''

plt.plot(rewards)
plt.xlabel('Epoch')
plt.ylabel('Rewards')
plt.show()