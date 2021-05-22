#!/usr/bin/env python3

import argparse
import datetime
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def prepDataFrame(orig_df):
    df = orig_df.copy()
    df['dow'] = 0
    df['Month'] = 0
    for index, row in df.iterrows():
        date = datetime.datetime.strptime(row['Date'], '%Y-%m-%d')
        df.dow[index] = datetime.datetime.strftime(date, '%w')
        df.Month[index] = datetime.datetime.strftime(date, '%m')
    return df

def calcHighLowWeekly(orig_df):
    df = orig_df.copy()
    df['WeekHigh'] = 0.0
    df['WeekLow'] = 0.0
    for index, row = df.iterrows():
        if index == 0:
            df.WeekHigh[index] = row['High']
            df.WeekLow[index] = row['Low']
        else:
            # Weekly info update
            if df.dow[index-1] > df.dow[index]:   # Account for the start of the week being either a Monday or a Tuesday after a 3 day weekend (prev day was Friday)
                df.WeekHigh[index] = row['High']
                df.WeekLow[index] = row['Low']
            else:
                df.WeekHigh_1[index] = df.WeekHigh_1[index-1]
                df.WeekLow_1[index] = df.WeekLow_1[index-1]

                # Weekly high
                prev_week_high = df.loc[index-1, 'WeekHigh_0']
                # If the current day's high is less than the previous week's high, then just copy the previous week's high
                if row['High'] < prev_week_high:
                    df.WeekHigh_0[index] = prev_week_high
                else:
                    # Otherwise, update all of the earlier days of the week with the current new high
                    df.WeekHigh_0[index] = row['High']
                    offset = 1
                    tmp_dow = df.dow[index]
                    tmp_dow_1 = df.dow[index - offset]
                    # While the previous day of the week is less than the current day (handles holidays)
                    while tmp_dow_1 < tmp_dow:
                        df.WeekHigh_0[index - offset] = row['High']
                        offset += 1
                        if offset > index:
                            break
                        tmp_dow = tmp_dow_1
                        tmp_dow_1 = df.dow[index - offset]

                # Weekly low
                prev_week_low = df.loc[index-1, 'WeekLow_0']
                if row['Low'] > prev_week_low:
                    df.WeekLow_0[index] = prev_week_low
                else:
                    df.WeekLow_0[index] = row['Low']
                    offset = 1
                    tmp_dow = df.dow[index]
                    tmp_dow_1 = df.dow[index - offset]
                    while tmp_dow_1 < tmp_dow:
                        df.WeekLow_0[index - offset] = row['Low']
                        offset += 1
                        if offset > index:
                            break
                        tmp_dow = tmp_dow_1
                        tmp_dow_1 = df.dow[index - offset]

    return new_df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", help="show program version", action="store_true")
    parser.add_argument("-o", "--outdir", help="output directory")
    parser.add_argument("datafile", help="stock OHLC data file")
    args = parser.parse_args()

    print(f"Processing {args.datafile}")
    df = pd.read_csv(args.datafile)

    df = prepDataFrame(df)

    # Set up columns for tracking higher level highs and lows
    df['MonthHigh_0'] = 0.0
    df['MonthLow_0'] = 0.0
    df['WeekHigh_1'] = 0.0
    df['WeekLow_1'] = 0.0
    df['MonthHigh_1'] = 0.0
    df['MonthLow_1'] = 0.0
    df['Day_0'] = '0'
    df['Week_0'] = '0'
    df['Month_0'] = '0'

    # Populate the dow and month information
    for index, row in df.iterrows():
        if index == 0:
            # Set up the first row as a baseline
            df.WeekHigh_0[index] = row['High']
            df.MonthHigh_0[index] = row['High']
            df.WeekLow_0[index] = row['Low']
            df.MonthLow_0[index] = row['Low']
        else:
            # Daily info update
            prev_open  = df.loc[index-1, 'Open']
            prev_high  = df.loc[index-1, 'High']
            prev_low   = df.loc[index-1, 'Low']
            prev_close = df.loc[index-1, 'Close']

            if row['High'] > prev_high:
                if row['Low'] < prev_low:
                    df.Day_0[index] = '3'
                else:
                    df.Day_0[index] = '2u'
            else:
                if row['Low'] < prev_low:
                    df.Day_0[index] = '2d'
                else:
                    df.Day_0[index] = '1'

            # Monthly info update
            if df.Month[index] != df.Month[index - 1]: # We have a new month
                df.MonthHigh_0[index] = row['High']
                df.MonthLow_0[index] = row['Low']
                df.MonthHigh_1[index] = df.MonthHigh_0[index-1]
                df.MonthLow_1[index] = df.MonthLow_0[index-1]
            else:
                df.MonthHigh_1[index] = df.MonthHigh_1[index-1]
                df.MonthLow_1[index] = df.MonthLow_1[index-1]

                # Monthly high
                prev_month_high = df.loc[index-1, 'MonthHigh_0']
                if row['High'] < prev_month_high:
                    df.MonthHigh_0[index] = prev_month_high
                else:
                    df.MonthHigh_0[index] = row['High']
                    offset = 1
                    tmp_month = df.Month[index]
                    tmp_month_1 = df.Month[index - offset]
                    while tmp_month_1 == tmp_month:
                        df.MonthHigh_0[index - offset] = row['High']
                        offset += 1
                        if offset > index:
                            break
                        tmp_month = tmp_month_1
                        tmp_month_1 = df.Month[index - offset]

                # Monthly Low
                prev_month_low = df.loc[index-1, 'MonthLow_0']
                if row['Low'] > prev_month_low:
                    df.MonthLow_0[index] = prev_month_low
                else:
                    df.MonthLow_0[index] = row['Low']
                    offset = 1
                    tmp_month = df.Month[index]
                    tmp_month_1 = df.Month[index - offset]
                    while tmp_month_1 == tmp_month:
                        df.MonthLow_0[index - offset] = row['Low']
                        offset += 1
                        if offset > index:
                            break
                        tmp_month = tmp_month_1
                        tmp_month_1 = df.Month[index - offset]

    print(df.head(30))

