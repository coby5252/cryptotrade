import GDAX
import time
import numpy as np


def gdax_accumulate_algo_1(open_target, profit_target, reset, eth_units, wait):
    key = 'a9527132122cef976696be5a7661039d'
    secret = 'qTsrkE/aOsRakhxdzFyMLb16FmYieaVUc146t1wOFneJvY2dKIr3c0uz+1oiLqWSCMe8is4uhg4G+RCjrIZhxw=='
    passphrase = '0g513yyqb2s'

    client = GDAX.AuthenticatedClient(key, str.encode(secret), passphrase, product_id="ETH-USD")

    try:
        open_buy = False
        open_sell = False

        time_since_buy = 0

        while True:
            if not open_buy and not open_sell:
                # no active orders.  open a new bid
                bid = get_bid(client)
                if bid == 0:
                        time.sleep(wait)
                        continue
                buyParams = {
                    'price': round(bid,2),
                    'size': round(eth_units,4),
                    'product_id': 'ETH-USD'
                }
                my_buy_order = client.buy(buyParams)['id']
                open_buy = True
                print("Opened buy position at %s"%(bid))
                time.sleep(wait)

            elif open_buy:
                try:
                    executed = client.getOrder(my_buy_order)['status'] == 'done'
                except:
                    executed = False # getOrder fails randomly

                if executed:
                    open_buy = False
                    print("Buy order closed")
                    ask = buyParams['price'] + .12
                    multiplier = buyParams['price'] / (ask)
                    sellParams = {
                        'price': round(ask, 2),
                        'size': round(multiplier * eth_units, 4),
                        'product_id': 'ETH-USD'
                    }
                    my_sell_order = client.sell(sellParams)['id']
                    open_sell = True
                    print("Opened sell position at %s"%(ask))
                    time.sleep(wait)
                else:
                    # Have not yet bought anything
                    if time_since_buy >= 900: # 15 minutes
                        client.cancelOrder(my_buy_order)
                        open_buy = False
                        time_since_buy = 0
                    else:
                        time.sleep(wait)
                        time_since_buy = time_since_buy + wait


            else: # open sell order
                try:
                    executed = client.getOrder(my_sell_order)['status'] == 'done'
                except:
                    executed = False # getOrder fails randomly

                if executed:
                    open_sell = False
                    print("Sell order closed")
                    bid = get_bid(client)
                    if bid == 0:
                        time.sleep(wait)
                        continue
                    buyParams = {
                        'price': round(bid,2),
                        'size': round(eth_units,4),
                        'product_id': 'ETH-USD'
                    }
                    my_buy_order = client.buy(buyParams)['id']
                    open_buy = True
                    print("Opened buy position at %s"%(bid))

                time.sleep(wait)

    except Exception as e:
        client.cancelAll()
        print("Exiting, %s"%(e))


def get_bid(client):
    highest = float(client.getProductOrderBook()['bids'][0][0])
    history = [x[4] for x in client.getProductHistoricRates()]
    mean = float(np.mean(history))
    sd = float(np.std(history))

    hi = mean + sd
    lo = mean - (2 * sd)

    if highest <= hi and highest >= lo:
        return round(highest - .02, 2)
    else:
        return 0


def get_ask(client):
    return get_bid(client) + .1


gdax_accumulate_algo_1(0, .03, .03, .5, 10)
