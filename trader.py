import market_profile as mp
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import asyncio
import time

STOCK_BASKET = ['ENTG', 'ESNT', 'GRBK', 'HMY', 'QRVO', 'NOVA', 'LAC', 'TSLA', 'ARKK', 'SHW']

def update_csv(tickers):
    '''
    Updates the stock data of all csv files
        @params: 
            tickers(list): list of tickers to be written to a file
        @return:
            closing list
    '''

    for ticker in tickers:
        data = yf.download(tickers=ticker, group_by='Close', interval='15m', period='45d')
        close = data['Close']
        close_list = close.to_csv('C:\python_projects\AlgoTrader\daily_data\stock_data_{ticker}.csv'.format(ticker=ticker))
    return close_list

def trade_algo():

    # Calculate Technical Indicators
    # Place trades
    market = mp.MarketProfile()
    for ticker in STOCK_BASKET:
        df = pd.read_csv('C:\python_projects\AlgoTrader\daily_data\stock_data_{}.csv'.format(ticker))
        macd = df.ta.macd()
        print(macd)
  
trade_algo()