#importing libraries
from flask import *
import hashlib
import sqlite3
import datetime
import ast
import uuid

#setting variables
app = Flask(__name__)

#home page
@app.route("/", methods=('GET', 'POST'))
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
