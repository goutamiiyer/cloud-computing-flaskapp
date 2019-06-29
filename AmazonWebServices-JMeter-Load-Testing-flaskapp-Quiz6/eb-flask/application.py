from flask import Flask, request, render_template
import os
import random
from math import radians, degrees, cos, sin, asin, sqrt
import csv, base64, time
import pymysql


application = Flask(__name__)

db = pymysql.connect(user='',
                     password='',
                     host='',
                     cursorclass=pymysql.cursors.DictCursor)
# Enter user, password and host. Deleted for security purposes
cursor = db.cursor()


@application.route("/")
def home():
    return render_template('home.html')


@application.route("/pop", methods=["POST", "GET"])
def pop():
    etime = []

    start_time = time.time()

    sql1 = "SELECT y2010 FROM dbo.pop WHERE state = 'Louisiana' OR state = 'Oklahoma' OR state = 'Texas'"
    cursor.execute(sql1)
    rows1 = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time-start_time
    etime.append(elapsed_time)
    return render_template("home.html", rows=rows1, rowcount=len(rows1), elapsed_time=elapsed_time)


if __name__ == "__main__":
    application.debug = True
    application.run()