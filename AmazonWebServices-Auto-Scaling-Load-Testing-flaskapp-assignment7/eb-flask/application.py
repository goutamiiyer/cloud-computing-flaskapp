from flask import Flask, request, render_template
import pandas as pd
import os
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


@application.route("/update", methods=["POST", "GET"])
def update():
    sid = int(request.form['sid'])
    course = int(request.form['course'])
    section = int(request.form['section'])

    start_time = time.time()

    sql1 = "SELECT idnum FROM dbo.st WHERE idnum = '" + str(sid) + "'"
    cursor.execute(sql1)
    rows1 = cursor.fetchall()

    sql2 = "SELECT maxseats FROM dbo.cr WHERE course = '" + str(course) + "' AND section = '" + str(section) + "' AND maxseats <> 0"
    cursor.execute(sql2)
    rows2 = cursor.fetchall()

    if rows1 and rows2 is not None:
        sql3 = "UPDATE dbo.cr SET maxseats = maxseats-1 WHERE course = '" + str(course) + "' AND section = '" + str(section) + "'"
        cursor.execute(sql3)
        sql4 = "INSERT INTO dbo.stco VALUES ('" + str(sid) + "', '" + str(course) + "', '" + str(section) + "')"
        cursor.execute(sql4)

    sql5 = "SELECT maxseats FROM dbo.cr WHERE course = '" + str(course) + "' AND section = '" + str(section) + "'"
    cursor.execute(sql5)
    rows5 = cursor.fetchall()

    sql6 = "SELECT * FROM dbo.stco"
    cursor.execute(sql6)
    rows6 = cursor.fetchall()

    sql7 = "SELECT sc.sid, sc.course, sc.section, c.maxseats FROM dbo.st as s, dbo.cr as c, dbo.stco as sc WHERE sc.sid=s.idnum AND sc.course=c.course AND sc.section=c.section"
    cursor.execute(sql7)
    rows7 = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time-start_time

    return render_template("update.html", rows1=rows1, rows2=rows2, rows5=rows5,rows6=rows6, rows7=rows7, elapsed_time=elapsed_time)


if __name__ == "__main__":
    application.debug = True
    application.run()