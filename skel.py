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

#print(df10.head(40))
df10.to_csv("../data/qqq.10min.txt")


