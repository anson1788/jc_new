import gym
from gym import spaces
import numpy as np


class cornerEnv(gym.Env):
    """A corner betting environment for OpenAI gym"""
    metadata = {'render.modes': ['human']}


    """
    ### Observation Space
    | Num | Observation                                                 | Min                | Max    | Unit |
    |-----|-------------------------------------------------------------|--------------------|--------|------|
    | 0   | time of the match                                           | 0                  | 120    | min  |
    | 1   | corner bet point                                            | 0                  | 25     | ball |
    | 2   | big odd                                                     | 1                  | 3      | ball |
    | 3   | small odd                                                   | 1                  | 3      | ball |
    | 4   | current corner point                                        | 0                  | 25     | ball |


    ### Action Space
    | Num | Action                                                     | Value   | Unit |
    |-----|-------------------------------------------------------------|---------|------|
    | 0   | Big                                                         | 0       | #    |
    | 1   | Dont buy                                                    | 1       | #    |
    | 2   | Small                                                       | 2       | #    |

    """
    def __init__(self, df):
        super(cornerEnv, self).__init__()
        self.df = df
        self.low = np.array([0, 0, 1, 1, 0], dtype=np.float32)
        self.high = np.array([125, 25, 3, 3, 25], dtype=np.float32)
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(self.low, self.high, dtype=np.float32)
        self.oddList = list()
        #print(self.observation_space)
        print("init end")
        
    def step(self, action):
        self.timeIdx = self.timeIdx + 1
        data = self.df[self.dfIdx].iloc[self.timeIdx]
        dataNext = self.df[self.dfIdx].iloc[self.timeIdx+1]
        stateA = ([
                      data["time"],
                      data["Point"],
                      data["High"],
                      data["Low"],
                      data["corner"]])
        done = False
        reward = 0
        if dataNext["time"]==-1:
            done = True
        '''
        if len(self.oddList) == 0 and action == 1:
            reward = -1
        if len(self.oddList) > 3 and action == 0:
            reward = -1
        if len(self.oddList) > 3 and action == 2:
            reward = -1
        '''
        if action == 0:
            self.oddList.append({
                "type":"big",
                "odd":data["High"],
                "point":data["Point"],
                "time":data["time"],
                "connerAt":data["corner"],
                })
        if action == 2:
            self.oddList.append({
                "type":"small",
                "odd":data["Low"],
                "point":data["Point"],
                "time":data["time"],
                "connerAt":data["corner"],
                })
        #if len(self.oddList) == 3:
            #done = True
            
        if done == True:
            reward = 0
            normalReward = 0 - len(self.oddList)
            result = self.df[self.dfIdx].iloc[-1]["corner"]
            print("result ",result)
            for idx in range(len(self.oddList)):
                if self.oddList[idx]["type"]=="small":
                    if self.oddList[idx]["point"] > result:
                        normalReward = normalReward + self.oddList[idx]["odd"]
                elif self.oddList[idx]["type"]=="big":
                    if result > self.oddList[idx]["point"] :
                        normalReward = normalReward + self.oddList[idx]["odd"]
            if len(self.oddList) == 0 :
                reward = -5
            else:
                reward = normalReward
       
        return stateA,reward,done,self.oddList

    def reset(self):
        isLoop = True
        while isLoop:
            self.dfIdx = np.random.randint(0, len(self.df))
            if len(self.df[self.dfIdx]) > 3:
                isLoop = False
            
        self.timeIdx = 2 
        self.oddList = list()
        print("Match IDX", self.dfIdx)
        #print("Match ", self.df[self.dfIdx])
        for idx in self.df[self.dfIdx].index:
            if self.df[self.dfIdx].iloc[idx]["High"] > 3:
                self.df[self.dfIdx].at[idx, "High"] = 3
            if self.df[self.dfIdx].iloc[idx]["Low"] > 3:
                self.df[self.dfIdx].at[idx, "Low"] = 3

        #state = ( self.get3State(self.timeIdx))
        return state

    def get3State(self, idx):
            data1 = self.df[self.dfIdx].iloc[idx]
            data2 = self.df[self.dfIdx].iloc[idx-1]
            data3 = self.df[self.dfIdx].iloc[idx-2]
            return [
                        [
                        data1["time"],
                        data1["Point"],
                        data1["High"],
                        data1["Low"],
                        data1["corner"]
                        ],
                        [
                        data2["time"],
                        data2["Point"],
                        data2["High"],
                        data2["Low"],
                        data2["corner"]
                        ],
                        [
                        data3["time"],
                        data3["Point"],
                        data3["High"],
                        data3["Low"],
                        data3["corner"]
                        ]
                    ]

    def render(self, mode='human', close=False):
        print("render")