import algo_trader as at
import market_profile as mp
import config


trader = at.AlgoTrader(config.universe)
profile = mp.MarketProfile()

''' Test Trader'''
trader.trade_macd()
#trader.setTicker('NVDA')
#trader.trade_loop()
#print(trader.get_security_price())

''' Test Orders '''
#profile.simple_order('NVDA', 10, 'buy', 'market', 'gtc')
#profile.close_position('NVDA')
#profile.bracket_buy('TSLA', 10, 'buy', 'market', 'gtc')