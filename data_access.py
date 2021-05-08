import csv
import yfinance as yf
import pandas as pd
import time


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


def update_single_csv(ticker):
    '''
    Updates the stock data of a single csv file
        @params: 
            ticker(str): ticker of file to be updated
    '''
    
    stock = yf.Ticker(ticker)
    data = stock.history(period='3mo', interval='1d')
    hist = pd.DataFrame(data=data, columns=['Close'])
    hist.reset_index(inplace=True)
    hist.to_csv('C:\python_projects\AlgoTrader\daily_data\stock_data_{ticker}.csv'.format(ticker=ticker))


def read_data(f_name):
    ''' Read csv into data frame'''
    df = pd.read_csv(f_name)
    return df

