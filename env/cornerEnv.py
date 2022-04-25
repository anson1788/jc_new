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
       
        stateA = ([
                      data["time"],
                      data["Point"],
                      data["High"],
                      data["Low"],
                      data["corner"]])
        done = False
        reward = 0
        if data["time"]==-1:
            done = True
        if len(self.oddList) == 0 and action == 1:
            reward = -1
        if len(self.oddList) > 3 and action == 0:
            reward = -1
        if len(self.oddList) > 3 and action == 2:
            reward = -1
        if action == 0:
            self.oddList.append({
                "type":"big",
                "odd":data["High"],
                "point":data["Point"]
                })
        if action == 2:
            self.oddList.append({
                "type":"big",
                "odd":data["Low"],
                "point":data["Point"]
                })
        if done == True:
            reward = 0
            normalReward = 0
            result = data["corner"]
            for idx in range(len(self.oddList)):
                if self.oddList[idx]["type"]=="small":
                    if result > self.oddList[idx]["point"]:
                        normalReward = normalReward + self.oddList[idx]["odd"]
                    else:
                        normalReward = normalReward - 1
                elif self.oddList[idx]["type"]=="big":
                    if result > self.oddList[idx]["point"]:
                        normalReward = normalReward - 1
                    else :
                        normalReward = normalReward + self.oddList[idx]["odd"]
            if len(self.oddList) == 0 :
                reward = -3
            else:
                reward = normalReward*2
       
        return stateA,reward,done,{}

        
    def reset(self):
        self.dfIdx = np.random.randint(0, len(self.df))
        self.timeIdx = 0 
        self.oddList = list()
        for idx in self.df[self.dfIdx].index:
            if self.df[self.dfIdx].iloc[idx]["High"] > 3:
                self.df[self.dfIdx].at[idx, "High"] = 3
            if self.df[self.dfIdx].iloc[idx]["Low"] > 3:
                self.df[self.dfIdx].at[idx, "Low"] = 3
        
        data = self.df[self.dfIdx].iloc[0]
        state = ([
                      data["time"],
                      data["Point"],
                      data["High"],
                      data["Low"],
                      data["corner"]])
        return state

    def render(self, mode='human', close=False):
        print("render")