#!/usr/bin/env python

import csv
from pandas_datareader import data as pdr
import argparse
import logging
import yfinance as yf

if __name__=='__main__':
    
    # Set up the parser to parse out the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('conf', help="Input configuration file")
    parser.add_argument('outdir', help="Output directory")
    args = parser.parse_args()

    yf.pdr_override()
    
    with open(f'{args.conf}') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            print(f'Pulling data for {row[0]}')
            data = pdr.get_data_yahoo(row[0])
            data.to_csv(f'{args.outdir}/{row[0]}.csv')
        print(f'Processed {line_count} lines.')
    
