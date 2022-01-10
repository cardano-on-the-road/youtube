#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 14:00:34 2019

@author: Valerio_Mellini
"""

import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from ta import add_all_ta_features
from ta.utils import dropna


#print (talib.get_functions())

class stocks_report:

    def __init__(self, stocks_path, days_offset = 1000):
        self.start_date = datetime.datetime.today() - datetime.timedelta(days=days_offset)
        self.end_date = datetime.datetime.today()
        data_list = pd.read_csv(stocks_path)
        self.ticker_list = data_list['Symbol']

    def start_job(self):
        first = True
        report = pd.DataFrame()
        for ticker in self.ticker_list:
            print(ticker)
            ticker_data = self.__get_data_from_yf(ticker)
            if ticker_data is not None:
                ticker_data = ticker_data.iloc[-1,:].to_frame().transpose().copy()
                ticker_data['Ticker'] = ticker
                ticker_data.set_index("Ticker", inplace=True)
                if first:
                    first = False
                    report = ticker_data.copy()
                else:
                    report = pd.concat([report, ticker_data])           
        return report
    
    def add_fundamental_data(self, df):
        ratios = ['trailingPE','marketCap', 'forwardEps', 'trailingEps', 'bookValue', 'priceToBook', 'pegRatio', 'sector', 'industry']
        new_df = df.reindex(columns = df.columns.tolist() + ratios)
        for row_index in new_df.index:
            try:
                print("Fundamental Ratios {0}".format(row_index))
                fund = yf.Ticker(row_index)
                info = fund.info
                for ratio in ratios:
                    value = info[ratio]
                    new_df.loc[row_index, ratio] = value
                    new_df["PercVolatility"] = new_df["Volatility"] /  new_df["Ma200"] * 100
            except:
                continue      
        new_df.sort_values(by=['pegRatio'])
        return new_df

    def __get_data_from_yf(self, ticker):
        try:
            downloaded_data = yf.download(ticker, start=self.start_date, end=self.end_date)
            df = downloaded_data.copy()
            df['Date'] = pd.to_datetime(df.index)
            df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            df['Ma21'] = df['Close'].rolling(21).mean()
            df['Ma50'] = df['Close'].rolling(50).mean()
            df['Ma200'] = df['Close'].rolling(200).mean()
            df['Volatility'] = df['Close'].rolling(200).std()
            df.dropna(inplace=True)
            df = add_all_ta_features(df, open="Open", high="High", low="Low", close="Close", volume="Volume")
            return df
        except Exception as e:
            print('Eccezione 1: {0}'.format(str(e)))
            return None


if __name__ == '__main__':
    s = stocks_report('./small_stocks.csv')
    report = s.start_job()
    new_report = s.add_fundamental_data(report)
    print('Task completed')

