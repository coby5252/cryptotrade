import sys
import os
import time
sys.path.append(os.path.abspath('../api'))
import GeminiRequest as api

def accumulate_algo_1(open_target, profit_target, reset, eth_units, wait):
    """This algorithm opens a buy at a certain level below market.  If
    and when that order is filled, it opens a sell order at a certain profit target"""

    api_client = api.GeminiRequest()
    try:
        open_buy = False
        open_sell = False

        time_since_buy = 0

        while True:
            bid = api_client.getPriceSpread()[0]
            if not open_buy and not open_sell:
                # no active orders.  open a new bid
                my_entry = bid - open_target
                my_buy_order = api_client.buy(eth_units, my_entry)['order_id']
                open_buy = True
                print("Opened buy position at %s"%(my_entry))
                time.sleep(wait)

            elif open_buy:
                executed = api_client.order_status(my_buy_order)['remaining_amount'] == '0'
                if executed:
                    open_buy = False
                    print("Buy order closed")
                    my_exit = my_entry + profit_target
                    multiplier = my_entry / (my_exit)
                    my_sell_order = api_client.sell(multiplier * eth_units, my_exit)['order_id']
                    open_sell = True
                    print("Opened sell position at %s"%(my_exit))
                    time.sleep(wait)
                else:
                    # Have not yet bought anything
                    if time_since_buy >= 1800: # 30 minutes
                        api_client.cancel_order(my_buy_order)
                        open_buy = False
                    else:
                        time.sleep(wait)
                        time_since_buy = time_since_buy + wait

            else: # open sell order
                executed = api_client.order_status(my_sell_order)['remaining_amount'] == '0'
                if executed:
                    open_sell = False
                    print("Sell order closed")
                    my_entry = bid - open_target - reset
                    my_buy_order = api_client.buy(eth_units, my_entry)['order_id']
                    open_buy = True
                    print("Opened buy position at %s"%(my_entry))
                    time.sleep(wait)
    except:
        api_client.cancel_all_orders()
        print("Exiting")

accumulate_algo_1(.2, 1, 2, .8, 10)

