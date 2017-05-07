import sqlite3

conn = sqlite3.connect('history.db')

def insert_price(connection, table, epoch_time, last, bid, ask, volume_24):
    c = connection.cursor()
    q = """INSERT INTO ? VALUES (?,?,?,?)"""
    vals = (epoch_time, last, bid, ask, volume_24)
    c.execute(q, vals)