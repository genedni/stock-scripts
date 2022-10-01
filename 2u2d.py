#!/usr/bin/python

import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

ohlc_dict = { 'Open' : 'first', 'High' : 'max', 'Low' : 'min', 'Close' : 'last' }
df = pd.read_csv("../data/qqq.1min.txt", parse_dates=['Date'], index_col=0) 

df10 = df.resample('10min').apply(ohlc_dict)
df10['Open'].replace('', np.nan, inplace=True)
df10.dropna(subset=['Open'], inplace=True)
df10['PrevOpen'] = df10['Open'].shift()
df10['PrevClose'] = df10['Close'].shift()

# Mark strat types
conditions = [ df10['PrevOpen'].gt(df10['Open']) & df10['PrevClose'].gt(df10['Close']), 
               df10['PrevOpen'].lt(df10['Open']) & df10['PrevClose'].lt(df10['Close']), 
               df10['PrevOpen'].gt(df10['Open']) & df10['PrevClose'].lt(df10['Close']),
               df10['PrevOpen'].lt(df10['Open']) & df10['PrevClose'].gt(df10['Close']),
               ]
choices = ['2d', '2u','1','3']
df10['Strat'] = np.select(conditions, choices)
df10['PrevStrat'] = df10['Strat'].shift()

#print(df10.head(40))
#df10.to_csv("../data/qqq.10min.txt")

for idx, row in df10.iterrows():
    print(idx, f"Open: {row['Open']} Prev Open: {row['PrevOpen']} Close: {row['Close']} Prev Close: {row['PrevClose']} Strat Type: {row['Strat']} Prev Strat: {row['PrevStrat']} ")


