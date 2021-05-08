import alpaca_trade_api as tradeapi
import algo_trader as at
import config


# MarketProfile provides basic access to Alpaca trading account
class MarketProfile:
    def __init__(self):
        # API calls
        self.paca = tradeapi.REST(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY,
                                  config.ALPACA_BASE_URL, api_version='v2')


    # Show Alpaca trading account balance
    def get_account_balance(self):
        account = self.paca.get_account()
        print('${} is available as buying power.'.format(account.buying_power))
        return account


    # Get a list of info on current orders and positions
    def list_info(self):
        # List of orders
        my_orders = self.paca.list_orders()
        if not my_orders:
            print("No active orders")
        else:
            print(my_orders)

        # List of positions
        my_positions = self.paca.list_positions()
        if not my_positions:
            print("No current positions")
        else:
            print(my_positions)
    

    # Close exisiting position on a stock
    def close_position(self, symbol):
        try:
            position = self.paca.get_position(symbol)
            print('Closing position for {}...\n'.format(symbol))
            self.paca.close_position(symbol)
        except:
            print('No positions held for {}\n'.format(symbol))


    # Place a simple order
    def simple_order(self, symbol, qty, side, type, time_in_force):
        # Get quote endpoint
        data = at.AlgoTrader(symbol)
        current_price = data.get_security_price()
        print(current_price)
        print('Placing order...')
        # Place an order
        self.paca.submit_order(
            symbol=symbol,
            side=side,
            type=type,
            qty=qty,
            time_in_force=time_in_force,
        )
        print('Bought 10 shares of {}\n'.format(symbol))


    # Place a bracket order
    def bracket_order(self, symbol, qty, side, type, time_in_force):
        # Get quote endpoint
        data = at.AlgoTrader(symbol)
        current_price = data.get_security_price(symbol)
        print(current_price)
        print('Placing order for {}'.format(symbol))
        # Place an order with stop loss @ -10%; take profit @ +2%
        self.paca.submit_order(
            symbol=symbol,
            side=side,
            type=type,
            qty=qty,
            time_in_force=time_in_force,
            order_class='bracket',
            stop_loss={'stop_price': current_price * 0.90,
                         'limit price': current_price * 0.91},
            take_profit={'limit_price': current_price * 1.02}
        )
        print('Bought 10 shares of {} with stop price @ -5% and limit @ +3%\n'.format(symbol))

    
        