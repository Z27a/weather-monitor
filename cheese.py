from flask import *
import hashlib
import sqlite3
from datetime import *
import ast
import uuid
import csv
db = "static/weather_user.db"

def create_connection(db_file):
    '''
    create a database connection to the SQLite database specified by db_file
    :param db_file: file path to database
    :return: connection to database
    '''
    #disconnect any previous connections
    conn = None
    #connect to db
    try:
        conn = sqlite3.connect(db_file)
    #print exception if there is one
    except Exception as e:
        print(e)
    #return connection
    return conn


def APIselectOrderTemp(conn):
    cur = conn.cursor()
    sql = f"select WindSpeed, WindDir, Datetime from WeatherData join Dates on Dates.TimeID = WeatherData.TimeID order by Timestamps desc limit 10"
    results = cur.execute(sql).fetchall()
    return(results)



conn = create_connection(db)
info = APIselectOrderTemp(conn)
html = ''
for item in info:
    html += f'''
           <tr>
                <td>{item[0]}<br></td>
                <td>{item[1]}<br></td>
                <td>{item[2]}<br></td>
            </tr>
            '''
print(html)