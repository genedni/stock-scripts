#!/usr/bin/env python3

import argparse
import pandas as pd
import yfinance as yf

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", help="show program version", action="store_true")
    parser.add_argument("-o", "--outdir", help="output directory")
    parser.add_argument("symbol", help="stock symbol to retrieve")
    args = parser.parse_args()

    if args.version:
        print("This is myprogram version 0.1")

    if args.outdir:
        print(f"Output directory: ${args.outdir}")
    else:
        print("Using current directory as output directory")
        args.outdir = "."

    print(f"Downloading {args.symbol}")
    df = yf.download(args.symbol, start='2021-01-01', progress=False)
    print(df.head())
    df.to_csv(f"{args.outdir}/{args.symbol}.csv")
