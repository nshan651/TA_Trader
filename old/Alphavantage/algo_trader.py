from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import pandas as pd
import matplotlib.pyplot as plt
import asyncio, datetime
import config 
import market_profile


# Trader using data from Alpha Vantage
class AlgoTrader:
    def __init__(self, universe):
        # Stock universe to be traded
        self.universe = universe
        # API calls
        self.tind = TechIndicators(key=config.ALPHA_VANTAGE_KEY, output_format='pandas') # Note: tech indicators does't support csv
        self.ts = TimeSeries(key=config.ALPHA_VANTAGE_KEY, output_format='pandas')
        self.mp = market_profile.MarketProfile()


    # Get the current price of a single security
    def get_security_price(self, symbol):
        data, meta = self.ts.get_quote_endpoint(symbol)
        df = pd.DataFrame(data=data)
        current_price = float(df.iloc[0][4])
        return current_price
        

    # Get MACD
    def macd(self, symbol):
        return self.tind.get_macd(symbol=symbol, interval='5min', series_type='close')


    # Logic to trade macd
    # Places a buy order if MACD is 2% above signal line, closes position if 2% below signal
    def trade_macd(self):
        for symbol in self.universe:
            big_mac, meta = self.macd(symbol)
            df = pd.DataFrame(big_mac, columns=['MACD','MACD_Signal', 'MACD_Hist'])
            # Get MACD and MACD Signal
            macd_data = float(df.iloc[0]['MACD'])
            signal_data = float(df.iloc[0]['MACD_Signal'])
          
            # TODO: Incorporate histograms
                       
            print('macd is: {}'.format(macd_data))
            print('signal is: {}'.format(signal_data))

            if (macd_data > signal_data*1.02):
                print('Trading on MACD')
                self.mp.bracket_order(symbol=symbol, qty=10, side='buy', type='market', time_in_force='gtc')
            elif (macd_data < signal_data*0.98):
                print('MACD is 2% below the signal, closing exisiting positions')
                self.mp.close_position(symbol)
            else:
                print('No trades made')

    
    # Initialize the trade loop: checks indicators every 5 minutes
    # call order:   trade_loop() --> update_indicators() --> trade_macd() --> *repeat until close
    def trade_loop(self): 
        loop = asyncio.get_event_loop()
        try:
            asyncio.ensure_future(self.update_indicators())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()


    # Check indicators every 5 minutes
    async def update_indicators(self):
        while True:
            print('\nchecking indicators...')
            self.trade_macd()
            await asyncio.sleep(300)