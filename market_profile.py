import alpaca_trade_api as tradeapi
import yfinance as yf
import config
import pandas as pd
import json


# MarketProfile provides basic access to Alpaca trading account
class MarketProfile:
    def __init__(self):
        # API calls
        self.paca = tradeapi.REST(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY,
                                  config.ALPACA_BASE_URL, api_version='v2')


    # Check if a position is held
    def has_position(self, symbol):
        try:
            position = self.paca.get_position(symbol)
            return True
        except:
            return False


    # Get the total value of the account
    def get_total_equity(self):
        account = self.paca.get_account()
        return float(account.equity)


    # Close exisiting position on a stock
    def close_position(self, symbol):
        try:
            position = self.paca.get_position(symbol)
            print('Closing position for {}...\n'.format(symbol))
            self.paca.close_position(symbol)
        except:
            print('No positions held for {}\n'.format(symbol))


    # Place a simple order
    def simple_order(self, symbol, qty, side, order_type, time_in_force):
        # Get quote endpoint
        current_price = self.get_price(symbol)
        print(current_price)
        print('Placing order...')
        # Place an order
        self.paca.submit_order(
            symbol=symbol,
            side=side,
            type=order_type,
            qty=qty,
            time_in_force=time_in_force,
        )
        print('Bought 10 shares of {}\n'.format(symbol))


    # Place a bracket order
    def bracket_order(self, symbol, side, order_type, time_in_force):
        # Get quote endpoint
        current_price = self.get_price(symbol)
        # Number of shares purchased is based off of the 10 stocks we are trading and 75% of portfolio value
        shares = int((((self.get_total_equity()*0.75)/10.0)/current_price))
        print('Placing order for {}'.format(symbol))
        # Place an order with stop loss @ -10%; take profit @ +1.5%
        self.paca.submit_order(
            symbol=symbol,
            side=side,
            type=order_type,
            qty=shares,
            time_in_force=time_in_force,
            order_class='bracket',
            stop_loss={'stop_price': current_price * 0.90,
                         'limit price': current_price * 0.91},
            take_profit={'limit_price': current_price * 1.015}
        )
        print('Bought {} shares of {} at {} per share with stop price @ -5% and limit @ +3%\n'.format(shares, symbol, current_price))


    # Get the current asking price using yfinance
    def get_price(self, ticker):
        stock =  yf.Ticker(ticker)
        current = stock.history(period='1d')
        return current['Close'][0]


    def get_portfolio(self):
    
        data = self.paca.get_portfolio_history(date_start="2021-04-05", timeframe='15Min', period='1M')
            
        print(data)
        return data


mp = MarketProfile()
#print(mp.get_total_equity())
mp.get_portfolio()
#mp.get_total_equity()
