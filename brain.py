#Mountain Car: Deep Q-Learning: Brain file

#Importing the libraries
import keras
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam 
from keras.layers import LSTM

#Building the Brain class
class Brain():
     
     def __init__(self, numInputs, numOutputs, lr):
          self.numInputs = numInputs
          self.numOutputs = numOutputs
          self.learningRate = lr
          
          #Creating the neural network
          self.model = Sequential()
          self.model.trainable = True
          self.model.add(Dense(units = 64, activation = 'relu', input_shape = (self.numInputs, )))
         ## self.model.add(LSTM(32, input_shape=(64,1)))
          self.model.add(Dense(units = 32, activation = 'relu'))
          
          self.model.add(Dense(units = self.numOutputs, activation='softmax'))
          
          self.model.compile(optimizer = Adam(lr = self.learningRate), loss = 'mse')


