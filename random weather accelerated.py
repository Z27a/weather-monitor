import random
from datetime import *
import time
import sqlite3

weatherDb = "static/weather_user.db"

timestamp = int(datetime.timestamp(datetime.now()))

try:
    conn = sqlite3.connect(weatherDb)
# print exception if there is one
except Exception as e:
    print(e)

for i in range(4032):

    t1 = round(random.uniform((25-2), 25), 2)
    t2 = round(random.uniform((t1-2), t1), 2)
    t3 = round(random.uniform((t2-3), t2), 2)
    wave = round(random.uniform(0.5, 3.5), 2)
    wind = round(random.uniform(5, 15), 2)
    windDir = round(random.uniform(20, 110), 2)
    lat = round(random.uniform(-16.898145, -16.898245), 6)
    long = round(random.uniform(145.821770, 145.822770), 6)

    cur = conn.cursor()

    sql = f"INSERT INTO Dates (Timestamps, Datetime) VALUES ({timestamp}, '{datetime.fromtimestamp(timestamp)}');"
    try:
        cur.execute(sql)
    except Exception as e:
        print(f"Timestamp {e}")
    conn.commit()
    timeID = cur.lastrowid

    sql = f"INSERT INTO WeatherData (Temp1, Temp2, Temp3, WaveHeight, WindSpeed, WindDir, Latitude, Longitude, TimeID)" \
          f"VALUES ({t1}, {t2}, {t3}, {wave}, {wind}, {windDir}, {lat}, {long}, {timeID});"
    try:
        cur.execute(sql)
    except Exception as e:
        print(f"WeatherData {e}")
    conn.commit()

    timestamp = timestamp + 300

conn.close()