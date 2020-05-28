#importing libraries
from flask import *
import hashlib
import sqlite3
from datetime import *
import ast
import uuid
import csv

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

#SQL statements and functions. Uses timestamp integers for time calculations.

def selectTemp(conn, depth, timestamp, repeats, period):
    cur = conn.cursor()
    results = ()
    for i in range(repeats):  #repeat the single select statement for the specified number of repeats and time periods.
        sql = f"select {depth} from WeatherData join Dates on Dates.TimeID = WeatherData.TimeID where Dates.Timestamps = {timestamp}"
        results = results + cur.execute(sql).fetchall()[0]
        timestamp = timestamp - period
    return(results)


def selectWindSpeed(conn, timestamp, repeats, period):
    cur = conn.cursor()
    results = ()
    for i in range(repeats):
        sql = f"select WindSpeed from WeatherData join Dates on Dates.TimeID = WeatherData.TimeID where Dates.Timestamps = {timestamp}"
        results = results + cur.execute(sql).fetchall()[0]
        timestamp = timestamp - period
    return(results)


def selectWave(conn, timestamp, repeats, period):
    cur = conn.cursor()
    results = ()
    for i in range(repeats):
        sql = f"select WaveHeight from WeatherData join Dates on Dates.TimeID = WeatherData.TimeID where Dates.Timestamps = {timestamp}"
        results = results + cur.execute(sql).fetchall()[0]
        timestamp = timestamp - period
    return(results)


#Simple select statements
def selectPword(conn, email):
    cur = conn.cursor()
    sql = f"select Password from Users where Email = '{email}'"
    results = cur.execute(sql).fetchall()[0]
    return(results)


def selectNames(conn, email):
    cur = conn.cursor()
    sql = f"select First_name, Last_name from Users where Email = '{email}'"
    results = cur.execute(sql).fetchall()[0]
    return(results)


def selectNewestTime(conn):
    cur = conn.cursor()
    sql = f"select  max(Timestamps) from Dates"
    results = cur.execute(sql).fetchall()[0][0]
    return(results)

#website routes/directories

#home page
@app.route("/", methods=('GET', 'POST'))
def index():
    #retrive graph data from the database.
    conn = create_connection(db)
    time = selectNewestTime(conn)
    Temp1 = selectTemp(conn, 'Temp1', time, 12, 2400)
    Temp2 = selectTemp(conn, 'Temp2', time, 12, 2400)
    Temp3 = selectTemp(conn, 'Temp3', time, 12, 2400)
    WindSpeed = selectWindSpeed(conn, time, 6, 57600)
    Wave = selectWave(conn, time, 13, 7200)

    #UNIMPLEMENTED ALTERNATE METHOD FOR GETTING DATA TO THE GRAPHS.
    # data = {
    #     type: 'line',
    #     'data': {
    #         'labels': [],
    #         'datasets': [{
    #             'label': '0m',
    #             'fill': True,
    #             'data': [],
    #             'backgroundColor': 'rgba(78, 115, 223, 0.05)',
    #             'borderColor': 'rgb(28,200,138)',
    #         },
    #             {
    #                 'label': '-2m',
    #                 'fill': True,
    #                 'data': [],
    #                 'backgroundColor': 'rgba(78, 115, 223, 0.05)',
    #                 'borderColor': 'rgb(54,185,204)',
    #             },
    #             {
    #                 'label': '-5m',
    #                 'fill': True,
    #                 'data': [],
    #                 'backgroundColor': 'rgba(78, 115, 223, 0.05)',
    #                 'borderColor': 'rgb(54,185,204)',
    #             }]
    #     },
    #     'options': {
    #         'maintainAspectRatio': False,
    #         'legend': {'display': True},
    #         'title': {},
    #         'scales': {
    #             'xAxes': [{
    #                 'gridLines':
    #                     {'color': 'rgb(234, 236, 244)',
    #                      'zeroLineColor': 'rgb(234, 236, 244)',
    #                      'drawBorder': False,
    #                      'drawTicks': False,
    #                      'borderDash': ['2'],
    #                      'zeroLineBorderDash': ['2'],
    #                      'drawOnChartArea': True},
    #                 'ticks': {
    #                     'fontColor': '#858796',
    #                     'beginAtZero': False,
    #                     'padding': 20}
    #             }],
    #             'yAxes': [{
    #                 'gridLines': {
    #                     'color': 'rgb(234, 236, 244)',
    #                     'zeroLineColor': 'rgb(234, 236, 244)',
    #                     'drawBorder': False,
    #                     'drawTicks': False,
    #                     'borderDash': ['2'],
    #                     'zeroLineBorderDash': ['2']},
    #                 'ticks': {
    #                     'fontColor': '#858796',
    #                     'beginAtZero': False,
    #                     'padding': 20}
    #             }]
    #         }
    #     }
    # }

    try:
        cookie = ast.literal_eval(request.cookies.get('userDetails'))
        userDetails = cookie[0]
    except:
        userDetails = 'Profile'
    #parse data into the html frontend.
    return render_template('index.html', Temp1=Temp1, Temp2=Temp2, Temp3=Temp3, WindSpeed=WindSpeed, Wave=Wave, userDetails=userDetails)


@app.route("/temperature", methods=('GET', 'POST'))
def temp():
    return render_template('tempTable.html')


@app.route("/wave", methods=('GET', 'POST'))
def wave():
    return render_template('waveTable.html')


@app.route("/wind", methods=('GET', 'POST'))
def wind():
    return render_template('windTable.html')


@app.route("/login", methods=('GET', 'POST'))
def login():
    # check method
    if request.method == 'POST':
        conn = create_connection(db)
        #requesting and checking info from html input forms.
        #first checks if both email and password are correct.
        if request.form['email'] and request.form['password']:
            email = request.form['email']
            pword = request.form['password']
            #encode input
            email = (hashlib.sha256(email.encode('utf-8'))).hexdigest()
            pword = (hashlib.sha256(pword.encode('utf-8'))).hexdigest()
            try:
                #get password from server
                serverPword = selectPword(conn, email)[0]
                #if passwords match
                if pword == str(serverPword):
                    #redirect to dashboard.
                    response = make_response(redirect(url_for("index")))
                    # set cookies with user details
                    names = selectNames(conn, email)
                    response.set_cookie("userDetails", f"{names[0]} {names[1]}")
                    return response
            except: # if not correct
                # set error message - currently not fully implemented.
                errorMsg = "Username or Password is incorrect."
                # reload page with error message
                return render_template('login.html', errorMsg=errorMsg)
    return render_template('login.html')


@app.route("/logout")
def logoutFn():
    #make cookie with redirect to main page
    response = make_response(redirect(url_for("index")))
    #set cookie to nothing, with immediate expiry
    response.set_cookie('userDetails', '', expires=0)
    return response


@app.route("/profile", methods=('GET', 'POST'))
def profileFn():
    return render_template('profile.html')


@app.route("/register", methods=('GET', 'POST'))
def registerFn():
    return render_template('register.html')

@app.route("/documentation", methods=('GET', 'POST'))
def docorFn():
    return render_template('documentation.html')
#API----------------------------------------------------------------------------------------------------------------------
#sql functions for API processes
def APIselectTemp(conn, timestamp, repeats, period):
    cur = conn.cursor()
    results = []
    #format and process data retreived from database
    for i in range(repeats):
        sql = f"select Temp1, Temp2, Temp3 from WeatherData join Dates on Dates.TimeID = WeatherData.TimeID where Dates.Timestamps = {timestamp}"
        #fetched sql data
        fetch = cur.execute(sql).fetchall()
        #average temps and put into tuple. Currently not used.
        avg = round(((fetch[0][0]+fetch[0][1]+fetch[0][2])/3),2)
        # add time to average temp tuple
        tt = (avg, str(datetime.fromtimestamp(int(timestamp))))
        #add temperature and time tuple to list
        final = [(fetch[0] + tt), ]
        #add more temperature elements to list
        results = results + final
        timestamp = timestamp - period
    return(results)


#return sorted temperatures
def APIselectOrderTemp(conn, repeats, orderItem, order):
    cur = conn.cursor()
    sql = f"select Temp1, Temp2, Temp3, Datetime from WeatherData join Dates on Dates.TimeID = WeatherData.TimeID order by {orderItem} {order} limit {repeats}"
    results = cur.execute(sql).fetchall()
    return(results)


#routes for the API
#rendering the temperature table on page load.
@app.route("/api/temperature/<repeats>", methods=('GET', 'POST'))
def APIgetTemps(repeats=0):
    if repeats != 0:
        conn = create_connection(db)
        info = APIselectTemp(conn, selectNewestTime(conn), int(repeats), 300)
        html = ''
        #insert data into html
        for item in info:
            html += f'''
                   <tr>
                        <td>{item[0]}<br></td>
                        <td>{item[1]}<br></td>
                        <td>{item[2]}<br></td>
                        <td>{item[4]}</td>
                    </tr>
                    '''
        #push html to the front end.
        return html


#download data as csv
@app.route("/api/download/<startDate>/<endDate>", methods=('GET', 'POST'))
def APIdownloadFile(startDate='', endDate=''):
    if startDate !='' and endDate != '':
        #write data to a csv file
        with open('output.csv', 'w', newline='') as csvfile:
            #set header names
            fieldnames = ['Time', 'Temperature (0m)', 'Temperature (-2m)', 'Temperature (-5m)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            #get data from database
            conn = create_connection(db)
            data = APIselectTemp(conn, selectNewestTime(conn), 500, 300)

            #write data
            writer.writeheader()
            for item in data:
                writer.writerow({'Time':item[4], 'Temperature (0m)':item[0], 'Temperature (-2m)':item[1], 'Temperature (-5m)':item[2]})
        #return file
    return  send_file('output.csv', attachment_filename='data.csv')


#rendering the temperature table with sorted values.
@app.route("/api/temperature/<repeats>/<orderItem>/<order>", methods=('GET', 'POST'))
def APIsortTemps(repeats=0, orderItem=0, order=0):
    if repeats != 0:
        conn = create_connection(db)
        info = APIselectOrderTemp(conn, int(repeats), orderItem, order)
        html = ''
        for item in info:
            html += f'''
                   <tr>
                        <td>{item[0]}<br></td>
                        <td>{item[1]}<br></td>
                        <td>{item[2]}<br></td>
                        <td>{item[3]}</td>
                    </tr>
                    '''
        return html

if __name__ == '__main__':
    app.run(debug=True)