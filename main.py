import data_access as dao
import market_profile as mp
import indicator as ind
import pandas as pd
import asyncio
import time


STOCK_BASKET = ['ENTG', 'ESNT', 'GRBK', 'HMY', 'QRVO', 'NOVA', 'LAC', 'TSLA', 'ARKK', 'SHW']


def main():
    trade_loop()


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
        ind.macd('C:\python_projects\AlgoTrader\daily_data\stock_data_{}.csv'.format(ticker), '15m')

    # Place trades
    market = mp.MarketProfile()
    for ticker in STOCK_BASKET:
        df = pd.read_csv('C:\python_projects\AlgoTrader\daily_data\stock_data_{}.csv'.format(ticker))
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


def trade_loop():
    '''
    Set up event loop and start placing trades
    trade_loop() --> update_indicators() --> trade_algo() -- Repeat
    '''
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(update_indicators())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


async def update_indicators():
    while True:
        print('\nchecking indicators...')
        trade_algo()
        await asyncio.sleep(900)


if __name__=='__main__':
    main()