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
    | 5   | point 1                                                     | -1                 | 25     | ball |
    | 6   | odd 1                                                       | 1                  | 3      | ball |
    | 7   | time 1                                                      | 0                  | 120    | ball |
    | 8   | point 2                                                     | -1                 | 25     | ball |
    | 9   | odd 2                                                       | 1                  | 3      | ball |
    | 10  | time 2                                                      | 0                  | 120    | ball |
    | 11  | point 3                                                     | -1                 | 25     | ball |
    | 12  | odd 3                                                       | 1                  | 3      | ball |
    | 13  | time 3                                                      | 0                  | 120    | ball |


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
        self.low = np.array([0, 0, 1, 1, 0,
                                -1,1,0,
                                -1,1,0,
                                -1,1,0], dtype=np.float32)
        self.high = np.array([125, 25, 3, 3, 25,
                                25,3,120,
                                25,3,120,
                                25,3,120], dtype=np.float32)
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(self.low, self.high, dtype=np.float32)
        self.oddList = list()
        #print(self.observation_space)
        print("init end")
        
    def step(self, action):
        data = self.df[self.dfIdx].iloc[self.timeIdx]
        dataNext = self.df[self.dfIdx].iloc[self.timeIdx+1]
        stateArray = [
                      dataNext["time"],
                      dataNext["Point"],
                      dataNext["High"],
                      dataNext["Low"],
                      dataNext["corner"],
                      1,
                      0,
                      0,
                      1,
                      0,
                      0,
                      1,
                      0,
                      0
                ]

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
        mapping = [5,8,11]
        for idx in range(len(self.oddList)):
            first = mapping[idx]
            sec = mapping[idx]+1
            thr = mapping[idx]+2

            if self.oddList[idx]["type"]=="small":
                 stateArray[first] = 2
                 stateArray[sec] = self.oddList[idx]["odd"]
                 stateArray[thr] = self.oddList[idx]["point"]
            elif self.oddList[idx]["type"]=="big":
                 stateArray[first] = 0
                 stateArray[sec] = self.oddList[idx]["odd"]
                 stateArray[thr] = self.oddList[idx]["point"]
            else:
                 stateArray[first] = 1
                 stateArray[sec] = 0
                 stateArray[thr] = 0
        done = False
        reward = 0
        if dataNext["time"]==-1:
            done = True          

        if len(self.oddList) == 3:
            done = True
            
        if done == True:
            reward = 0
            normalReward = 0 - len(self.oddList)
            result = self.df[self.dfIdx].iloc[-1]["corner"]
            #print("result ",result)
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
        else:
            self.timeIdx = self.timeIdx + 1
            reward = -0.02
        stateA = (stateArray)
        return stateA,reward,done,self.oddList

    def reset(self):
        self.dfIdx = np.random.randint(0, len(self.df))
        self.timeIdx = 0 
        #print("Match IDX", self.dfIdx)
        #print("Match ", self.df[self.dfIdx])
        for idx in self.df[self.dfIdx].index:
            if self.df[self.dfIdx].iloc[idx]["High"] > 3:
                self.df[self.dfIdx].at[idx, "High"] = 3
            if self.df[self.dfIdx].iloc[idx]["Low"] > 3:
                self.df[self.dfIdx].at[idx, "Low"] = 3
        
        data = self.df[self.dfIdx].iloc[0]
        self.oddList = list()
        state = ([
                      data["time"],
                      data["Point"],
                      data["High"],
                      data["Low"],
                      data["corner"],
                      1,
                      0,
                      0,
                      1,
                      0,
                      0,
                      1,
                      0,
                      0
                ])
        return state

    def render(self, mode='human', close=False):
        print("render")