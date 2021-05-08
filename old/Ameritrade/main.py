import market_profile
import ameritrader
import config

mp = market_profile.MarketProfile()
mp.bracket_order('SPY', 10, 'buy', 'market', 'gtc')