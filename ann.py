from os import listdir
from os.path import isfile, isdir, join
import datetime
import json
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from tensorflow.keras.optimizers import Adam 
import numpy
from tensorflow import keras
mypath = "/Users/hello/jc_new2/setData/result.xlsx"
df = pd.read_excel(mypath)


endGoal = []
result = []
inputData = []
for index, row in df.iterrows():
    if index > 60:
        item = df.iloc[index]
        inputData.append(numpy.array([
            item["high"],item["startPoint"],item["low"],item["mHigh"],item["midPoint"],item["mLow"]  ]))
        if row['midPoint'] > row['endResult']:
            endGoal.append(numpy.array([0,1]))
            result.append("small")
        else:
            endGoal.append(numpy.array([1,0]))
            result.append("big")

yTrain = numpy.array(endGoal)
xTrain = numpy.array(inputData)



model = keras.models.load_model("/Users/hello/jc_new2/ann58")
yVal = model.predict(xTrain)
predictY = []
for idx in range(yVal.shape[0]):
    if format(yVal[idx][1],'f') >format(yVal[idx][0],'f'):
        predictY.append("small")
    else:
        predictY.append("big")
print(predictY)
correctIdx = 0
for idx in range(len(predictY)):
    if result[idx] == predictY[idx]:
        correctIdx = correctIdx + 1
print(correctIdx , " ", len(predictY))

'''
model = Sequential()
model.trainable = True
model.add(Dense(units = 24, activation = 'sigmoid', input_shape = (6, )))
model.add(Dropout(0.2))
model.add(Dense(units = 48, activation = 'sigmoid'))
model.add(Dropout(0.2))
model.add(Dense(units = 36, activation = 'sigmoid'))
model.add(Dropout(0.2))
model.add(Dense(units = 24, activation = 'sigmoid'))
model.add(Dropout(0.2))
model.add(Dense(units = 12, activation = 'sigmoid'))
model.add(Dropout(0.2))
model.add(Dense(units = 2 ,activation='sigmoid'))
#model.compile(loss="binary_crossentropy", optimizer="RMSprop")
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(xTrain, yTrain, epochs=150000, batch_size=5)
model.save("/Users/hello/jc_new2/ann58")
'''