#!/usr/bin/env python

import csv
from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()
outdir = 'test'

with open('data/n100.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        line_count += 1
        print(f'Pulling data for {row[0]}')
        data = pdr.get_data_yahoo(row[0])
        data.to_csv(f'{outdir}/{row[0]}.csv')
    print(f'Processed {line_count} lines.')
