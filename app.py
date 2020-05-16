#TODO fix broken graphs
#TODO update data tags

#importing libraries
from flask import *
import hashlib
import sqlite3
from datetime import *
import ast
import uuid

#setting variables
app = Flask(__name__)

weatherDb = "static/weather_user.db"

timestamp = float(datetime.timestamp(datetime.now()))

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


def selectTemp(conn, depth, timestamp, repeats, period):
    cur = conn.cursor()
    results = ()
    for i in range(repeats):
        sql = f"select {depth} from Link join Temperature on Temperature.TempID = Link.TempID join Dates on Dates.TimeID=Link.TimeID where Dates.timestamps = {timestamp}"
        results = results + cur.execute(sql).fetchall()[0]
        timestamp = timestamp - period
    return(results)


def selectWindSpeed(conn, timestamp, repeats, period):
    cur = conn.cursor()
    results = ()
    for i in range(repeats):
        sql = f"select Windspeed from Link join Wind on Wind.WindID = Link.WindID join Dates on Dates.TimeID=Link.TimeID where Dates.timestamps = {timestamp}"
        results = results + cur.execute(sql).fetchall()[0]
        timestamp = timestamp - period
    return(results)



def selectWave(conn, timestamp, repeats, period):
    cur = conn.cursor()
    results = ()
    for i in range(repeats):
        sql = f"select WaveHeight from Link join Wave on Wave.WaveID = Link.WaveID join Dates on Dates.TimeID=Link.TimeID where Dates.timestamps = {timestamp}"
        results = results + cur.execute(sql).fetchall()[0]
        timestamp = timestamp - period
    return(results)

#home page
@app.route("/", methods=('GET', 'POST'))
def index():
    conn = create_connection(weatherDb)
    Temp1 = selectTemp(conn, 'Temp1', 1590815510.873754, 12, 2400)
    Temp2 = selectTemp(conn, 'Temp2', 1590815510.873754, 12, 2400)
    Temp3 = selectTemp(conn, 'Temp3', 1590815510.873754, 12, 2400)
    WindSpeed = selectWindSpeed(conn, 1590815510.873754, 6, 57600)
    Wave = selectWave(conn, 1590815510.873754, 13, 7200)

    return render_template('index.html', Temp1=Temp1, Temp2=Temp2, Temp3=Temp3, WindSpeed=WindSpeed, Wave=Wave)

if __name__ == '__main__':
    app.run(debug=True)
