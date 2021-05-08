import requests
import json
import pandas as pd
import config
import time
        

''' Get the latest price of a stock '''
def get_current_price(ticker):
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{}/quotes?'.format(ticker)
    page = requests.get(url=endpoint, params={'apikey': config.AMERITRADE_KEY})
    content = json.loads(page.content)
    df = pd.DataFrame(data=content)
    return float(df.loc['regularMarketLastPrice'])


''' Get the previous closing price '''
def get_close(ticker):
    df = get_history(ticker,'month', 1,'daily',1)
    print(df)
    return float(df.loc[0]['close'])


''' Get the price history '''
def get_history(ticker, periodType, period, frequencyType, frequency): 
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory?periodType={periodType}' \
        '&period={period}&frequencyType={frequencyType}&frequency={frequency}'.format(
            ticker=ticker, periodType=periodType, period=period, frequencyType=frequencyType, frequency=frequency)
    page = requests.get(url=endpoint, params={'apikey': config.AMERITRADE_KEY})
    content = json.loads(page.content)
    df = pd.json_normalize(content, record_path=['candles'])
    return df


''' 
--- Caluclate the Simple Moving Average --- 
SMA = An/n 
'''
def sma(ticker, num):
    # Get current Epoch time in ms
    current_time = round(time.time()*1000)
    # Get the range of days; converted to ms
    num_range = current_time - (num*86400000)
    # Get the Historical DataFrame
    df = get_history(ticker=ticker, periodType='month', period=2, frequencyType='daily', frequency=1)
    # Set the iterator to the total number of rows, 
    i=len(df)-1
    total =0 
    count =0
    # While the date time is greater than the date range, retrieve the sum and count
    while (df.iloc[i]['datetime'] >= num_range):
        total += df.iloc[i]['close']
        print('datetime iter: {}'.format(df.iloc[i]['datetime']))
        count+=1 
        i+=1
    val = total/count
    return val


''' 
--- Calculate the Exponential Moving Average --- 
EMA = (Current Value * (Smoothing/1+Days)) + Previous EMA * (1-(Smoothing/1+Days)))
NOTE: Use SMA if there is no previous EMA; Smoothing factor is 2 because it gives recent observations more weight
'''
def ema(ticker, num):
    ema_prev = 0
    ema_list = []
    for i in range (num, 0, -1):
        # If there is no existing ema, use sma, else use previous ema
        if (ema_prev==0):
            ema_prev = sma(ticker, num)  
            print(ema_prev)
        print('ema_prev is: {}'.format(ema_prev))
        # Get the current price; this will be a stand-in for closing price
        close = get_current_price(ticker) #TODO: CHANGE THIS 
        # Get the smoothing factor
        factor = (2/(num+1))
        val = (close * factor) + (ema_prev*(1-factor))
        ema_list.append(round(val, 4))
        ema_prev=round(val, 4)
        #count=count-1
    return ema_list


''' 
--- Calculate the MACD ---
MACDE = 12-Period EMA - 26-Period EMA
'''
def macd(ticker):
    ema_12 = ema(ticker, 12)
    ema_26 = ema(ticker, 26)
    macd = ema_12 - ema_26
    signal = macd_signal(ticker, macd)
    return round(macd, 4), signal


''' 
--- Calculate the MACD 9-Period Signal ---
Take the 9-Period EMA of the MACD
'''
def macd_signal(ticker, macd_val):
    ema_prev = macd_val
    # Get the current price; this will be a stand-in for closing price
    # TODO: Switch this to previous mkt close
    current = get_current_price(ticker)
    # Get the smoothing factor
    factor = (1/5) # (2/(9+1) = 1/5)
    val = (current * factor) + (ema_prev*(1-factor))
    return round(val, 4)


''' TEST BLOCK '''
#get_history(ticker='SPY', periodType='month', period=1, frequencyType='daily', frequency=1)
#print(get_history(ticker='SPY', periodType='month', period=2, frequencyType='daily', frequency=1))
#sma('SPY', 5)
#print(ema('SPY', 5))
print(get_close('SPY'))