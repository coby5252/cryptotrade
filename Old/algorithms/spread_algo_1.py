import sys
import os
import time
sys.path.append(os.path.abspath('../api'))
import GeminiRequest as api

def spread_algo_1(spread_threshold, eth_units, wait):
    """Algorithm that checks the bid/ask spread on Gemini for ETH/USD
    If the spread is large enough, we will buy and sell ether within 
    the spread.  If the spread tightens, then we will cnacel our orders.
    If both orders are filled, we will re-up as long as the spread persists.
    The goal of this alogirithm is to accumulate ETH"""

    api_client = api.GeminiRequest()
    open_buy = False
    open_sell = False

    while True:
        bid = api_client.getPriceSpread()[0]
        ask = api_client.getPriceSpread()[1]
        spread = ask - bid

        if(open_buy or open_sell):
            # Buy side
            executed = api_client.order_status(my_buy_order)['remaining_amount'] == '0'
            if not executed:
                if bid > my_bid:
                    api_client.cancel_order(my_buy_order)
                    my_buy_order = api_client.buy(eth_units, bid + .01)
                    print(my_buy_order)
                    my_buy_order = my_buy_order['order_id']
                    my_bid = bid + .01
                    print("Adjusted buy to %s"%(my_bid))
                else:
                    print("Buy still open")
            else:
                open_buy = False


            # Sell side
            executed = api_client.order_status(my_sell_order)['remaining_amount'] == '0'
            if not executed:
                if ask < my_ask:
                    api_client.cancel_order(my_sell_order)
                    my_sell_order = api_client.sell(eth_units, ask - .01)
                    print(my_sell_order)
                    my_sell_order = my_sell_order['order_id']
                    my_ask = ask - .01
                    print("Adjusted sell to %s"%(my_ask))
                else:
                    print("Sell still open")
            else:
                open_sell = False
            time.sleep(wait)

        elif(spread > spread_threshold):
            if not open_buy and not open_sell: # no open orders
                my_buy_order = api_client.buy(eth_units, bid + .01)
                print(my_buy_order)
                my_buy_order = my_buy_order['order_id']
                my_sell_order = api_client.sell(eth_units, ask - .01)
                print(my_sell_order)
                my_sell_order = my_sell_order['order_id']
                open_buy = True
                open_sell = True
                my_bid = bid + .01
                my_ask = ask - .01
                print("Opened positions at %(buy)s and %(sell)s"%{'buy': my_bid, 'sell': my_ask})
                time.sleep(wait)

            else:
                time.sleep(wait)

        else:
            api_client.cancel_all_orders()
            open_buy = False
            open_sell = False
            time.sleep(wait)

spread_algo_1(.2, 1.5, 1)