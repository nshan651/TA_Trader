import data_access as dao
import market_profile as mp
import indicator as ind
import pandas as pd
import asyncio
import time
import threading


STOCK_BASKET = ['ENTG', 'ESNT', 'GRBK', 'HMY', 'QRVO', 'NOVA', 'LAC', 'TSLA', 'ARKK', 'SHW']


def main():
    asyncio.run(update_indicators())


def trade_algo():
    '''
    MACD Crossover: 
        - if the MACD is above the signal line by 0.05 or more, place a trade
        - else if MACD is below the signal line by 1 or more, close existing positions
    '''

    # Update csv
    dao.update_csv(STOCK_BASKET)

    # Compute macd
    for ticker in STOCK_BASKET:
        ind.macd(f'/home/nick/git/TA_Trader/daily_data/stock_data_{ticker}.csv', '15m')

    # Place trades
    market = mp.MarketProfile()
    for ticker in STOCK_BASKET:
        df = pd.read_csv(f'/home/nick/git/TA_Trader/daily_data/stock_data_{ticker}.csv')
        hist = df.iloc[len(df)-1]['Hist']
        if (hist > 0.05):
            print('MACD is for {} is above the signal line, attempting to placing trade'.format(ticker))
            if (not market.has_position(ticker)):
                market.bracket_order(symbol=ticker, side='buy', order_type='market', time_in_force='gtc')
            else:
                print('Already hold shares of {}, no trades made'.format(ticker))
        elif (hist < -1):
            print('Downward momentum for {}, closing existing position'.format(ticker))
            market.close_position(ticker)
        else:
            print('MACD is neutral for {}, no trades made\n'.format(ticker))


async def update_indicators():
    while True:
        print('\nchecking indicators...')
        trade_algo()
        await asyncio.sleep(900)


if __name__=='__main__':
    main()
