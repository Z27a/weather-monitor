import random
from datetime import *
import time
import sqlite3

weatherDb = "static/weather_user.db"

timestamp = datetime.timestamp(datetime.now())

for i in range(4032):

    try:
        conn = sqlite3.connect(weatherDb)
    #print exception if there is one
    except Exception as e:
        print(e)


    t1 = round(random.uniform((25-2), 25), 2)
    t2 = round(random.uniform((t1-2), t1), 2)
    t3 = round(random.uniform((t2-3), t2), 2)
    wave = round(random.uniform(0.5, 3.5), 2)
    wind = round(random.uniform(5, 15), 2)
    windDir = round(random.uniform(20, 110), 2)
    lat = round(random.uniform(-16.898145, -16.898245), 6)
    long = round(random.uniform(145.821770, 145.822770), 6)

    cur = conn.cursor()

    sql = f"INSERT INTO Dates (Timestamps)" \
          f"VALUES ({timestamp});"
    try:
        cur.execute(sql)
    except Exception as e:
        print(f"Timestamp {e}")
    conn.commit()
    timeID = cur.lastrowid

    sql = f"INSERT INTO Temperature (Temp1, Temp2, Temp3)" \
          f"VALUES ({t1}, {t2}, {t3});"
    try:
        cur.execute(sql)
    except Exception as e:
        print(f"Temperature {e}")
    conn.commit()
    tempID = cur.lastrowid

    sql = f"INSERT INTO Wave (WaveHeight)" \
          f"VALUES ({wave});"
    try:
        cur.execute(sql)
    except Exception as e:
        print(f"Wave {e}")
    conn.commit()
    waveID = cur.lastrowid

    sql = f"INSERT INTO Wind (WindSpeed, WindDir)" \
          f"VALUES ({wind}, {windDir});"
    try:
        cur.execute(sql)
    except Exception as e:
        print(f"Wind {e}")
    conn.commit()
    windID = cur.lastrowid

    sql = f"INSERT INTO Location (Latitude, Longitude)" \
          f"VALUES ({lat}, {long});"
    try:
        cur.execute(sql)
    except Exception as e:
        print(f"Wind {e}")
    conn.commit()
    locationID = cur.lastrowid


    sql = f"INSERT INTO Link (TimeID, TempID, WaveID, WindID, LocationID)" \
          f"VALUES ({timeID}, {tempID}, {waveID}, {windID}, {locationID});"
    try:
        cur.execute(sql)
    except Exception as e:
        print(f"Wind {e}")
    conn.commit()

    conn.close()

    timestamp = timestamp + 300
