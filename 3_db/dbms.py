import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def fetch_data():
    con = sqlite3.connect("sensordata.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT * FROM DHT22_DATA")
    # print(cur.fetchall())
    list_of_dicts = cur.fetchall()
    con.close()
    d = json.dumps(list_of_dicts)
    return d

def store_data(data):
    d = dict(param.split('=') for param in data.split('&'))
    conn = sqlite3.connect("sensordata.db")
    conn.execute("CREATE TABLE IF NOT EXISTS DHT22_DATA (id integer primary key, time datetime, temperature real, humidity real, hic real)")
    conn.execute("INSERT INTO DHT22_DATA(time, temperature, humidity, hic) values (datetime(current_timestamp,'localtime'), "+d['temperature']+", "+d['humidity']+", "+d['hic']+")")
    conn.commit()
    conn.close()
