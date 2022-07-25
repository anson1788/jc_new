from os import listdir
from os.path import isfile, isdir, join
import datetime
import json
import pandas as pd

mypath = "D:\\jc_new\\excelData"
#allJson = "D:\\jc_new\\combine\\all.json"
#mypath = "/Users/hello/jc_new/data"
#allJson = "/Users/hello/jc_new/combine/all.json"
files = listdir(mypath)

dataList = []
for f in files:
    fullpath = join(mypath, f)
    if ".xlsx" in f: 
        fileNameTime = f.replace(".xlsx", "")
        df = pd.read_excel(fullpath)
        df['matchID'] = fileNameTime
        dataList.append(df)

for f in dataList:
    dataLength = f[f.columns[0]].count()
    print( f.iloc[0]['matchID']," " ,f.iloc[dataLength-2]["time"]," ",f.iloc[0]["time"] , "=", f.iloc[dataLength-2]["time"])