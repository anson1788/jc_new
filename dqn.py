#Mountain Car: Deep Q-Learning - Experience Replay Memory file

#Initializing the Experience Replay Memory
import numpy as np

class Dqn():
     
     def __init__(self, maxMemory, discount):
          self.maxMemory = maxMemory
          self.discount = discount
          self.memory = list()
          
     #Remembering new experience
     def remember(self, transition, gameOver):
          #print("transition",transition)
          self.memory.append([transition, gameOver])
          if len(self.memory) > self.maxMemory:
               del self.memory[0]
     
     #Getting batches of inputs and targets
     def getBatch(self, model, batchSize):
          lenMemory = len(self.memory)
          numInputs = len(self.memory[0][0][0])
          numOutputs = model.output_shape[-1]
          
          #Initializing the inputs and targets
          inputs = np.zeros((min(batchSize, lenMemory), numInputs))
          targets = np.zeros((min(batchSize, lenMemory), numOutputs))
          
          #Extracting transitions from random experiences 
          for i, inx in enumerate(np.random.randint(0, lenMemory, size = min(batchSize, lenMemory))):
          #for i in range(min(batchSize, lenMemory)):
               currentState, action, reward, nextState = self.memory[i][0]
               gameOver = self.memory[i][1]
               #Updating inputs and targets
               inputs[i] = np.array([currentState]) 
               nexStateNp = np.array([nextState])
               targets[i] = model.predict(np.array([currentState]))[0]
               if gameOver:
                    targets[i][action] = reward
               else:
                    targets[i][action] = reward + self.discount * np.max(model.predict(nexStateNp)[0])
          
          return inputs, targets
               
          
     
          
     
     
     
















