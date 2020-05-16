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

db = "static/weather_user.db"

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
    conn = create_connection(db)
    Temp1 = selectTemp(conn, 'Temp1', 1590815510.873754, 12, 2400)
    Temp2 = selectTemp(conn, 'Temp2', 1590815510.873754, 12, 2400)
    Temp3 = selectTemp(conn, 'Temp3', 1590815510.873754, 12, 2400)
    WindSpeed = selectWindSpeed(conn, 1590815510.873754, 6, 57600)
    Wave = selectWave(conn, 1590815510.873754, 13, 7200)

    return render_template('index.html', Temp1=Temp1, Temp2=Temp2, Temp3=Temp3, WindSpeed=WindSpeed, Wave=Wave)

@app.route("/temperature", methods=('GET', 'POST'))
def temp():
    return render_template('tempTable.html')




def APIselectTemp(conn, timestamp, repeats, period):
    cur = conn.cursor()
    results = []
    for i in range(repeats):
        sql = f"select Temp1, Temp2, Temp3 from Link join Temperature on Temperature.TempID = Link.TempID join Dates on Dates.TimeID=Link.TimeID where Dates.timestamps = {timestamp}"
        #fetched sql data
        fetch = cur.execute(sql).fetchall()
        print(fetch)
        #average temps and put into tuple
        avg = round(((fetch[0][0]+fetch[0][1]+fetch[0][2])/3),2)
        print(avg)
        # add time to average temp tuple
        tt = (avg, str(datetime.fromtimestamp(int(timestamp))))
        print(tt)
        #add temperature and time tuple to list
        final = [(fetch[0] + tt), ]
        print(final)
        #add more temperature elements to list
        results = results + final
        timestamp = timestamp - period
    return(results)


@app.route("/api/temperature", methods=('GET', 'POST'))
def APIgetTemps():
    conn = create_connection(db)
    print(APIselectTemp(conn, 1590815510.873754, 10, 300))
    return "hello?"

if __name__ == '__main__':
    app.run(debug=True)
