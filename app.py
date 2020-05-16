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


def selectTemp(conn, depth, timestamp):
    cur = conn.cursor()
    results = ()
    for i in range(12):
        sql = f"select {depth} from Link join Temperature on Temperature.TempID = Link.TempID join Dates on Dates.TimeID=Link.TimeID where Dates.timestamps = {timestamp}"
        results = results + cur.execute(sql).fetchall()[0]
        timestamp = timestamp - 2400
    return(results)

#home page
@app.route("/", methods=('GET', 'POST'))
def index():
    conn = create_connection(weatherDb)
    Temp1 = selectTemp(conn, 'Temp1', 1590815510.873754)
    print(Temp1)

    return render_template('index.html', temps=Temp1)

if __name__ == '__main__':
    app.run(debug=True)
