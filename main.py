import sys
import os
sys.path.append(os.path.abspath('./algorithms'))
sys.path.append(os.path.abspath('./api'))
sys.path.append(os.path.abspath('./database'))
import PlusMinusStdevAlgorithm as algo
import GeminiRequest as api
import Database as db

def main():
    """Log prices into a database, unless an api request can replace this"""
    time = int(time.time()) # epoch time in seconds
    price = api.getLastPrice()
    db.insert_price(table = 'tbl_eth_price_history', time = time, price = price) # do this every x seconds.. 60?

    """Run the trading algorithm"""
    algo.run()

    """Stop the trading algorithm"""
    algo.stop() # Safely exit all positions and stop the algorithm

    """Rebalance account balances"""
    api.rebalance() # Do this if ETH/USD ratio gets above or below certain amount

main()
    