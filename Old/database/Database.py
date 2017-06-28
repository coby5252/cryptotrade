import sqlite3
import os

db_file = os.path.join(os.path.dirname(__file__), 'history.db')
conn = sqlite3.connect(db_file)

def insert_price(table, epoch_time, last, bid, ask, volume_24, connection = conn):
    c = connection.cursor()
    vals = (int(epoch_time), round(last, 2), round(bid,2), round(ask,2), round(volume_24, 2))
    c.execute("INSERT INTO %s VALUES (?,?,?,?,?)"%(table), vals)
    connection.commit()
    connection.close()
