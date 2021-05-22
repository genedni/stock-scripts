#!/usr/bin/env python3

import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stock_file', help='location of the stock file to process')
    parser.add_argument('-o', '--outdir', help='location of the output directory')
    args = parser.parse_args()

    print(f"Conf file: {args.stock_file}")
    print(f"Output directory: {args.outdir}")

    with open(args.stock_file, "r") as rf:
        # Read each line of a file in the loop
        for symbol in rf:
            print(f"Processing {symbol}")
            output = os.system(f"getstock.py -o {args.outdir} {symbol}")
