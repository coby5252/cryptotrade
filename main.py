import sys
import os
import threading
sys.path.append(os.path.abspath('./algorithms'))
sys.path.append(os.path.abspath('./api'))
sys.path.append(os.path.abspath('./database'))
import PlusMinusStdevAlgorithm as algo
import GeminiRequest as api
import Database as db

def main():
    """Log prices into a database, unless an api request can replace this"""
    db_insert_price()
    
    """Run the trading algorithm"""
    algo.run()

    """Stop the trading algorithm"""
    algo.stop() # Safely exit all positions and stop the algorithm

    """Rebalance account balances"""
    api.rebalance() # Do this if ETH/USD ratio gets above or below certain amount


def db_insert_price():
    """Log prices into a database, unless an api request can replace this"""
    epoch_time = int(time.time() * 1000) # epoch time in seconds
    req = api.GeminiRequest()
    last = req.getLastPrice()
    bid, ask = req.getPriceSpread()
    volume_24 = req.getVolume()
    db.insert_price(table = 'tbl_eth_price_history', time = time, price = price)
    threading.Timer(60, db_insert_price).start()


main()
    