from flask import Flask, request, render_template
import pandas as pd
import os
from math import radians, degrees, cos, sin, asin, sqrt
import csv, base64, time
import datetime
import pymysql



application = Flask(__name__)

db = pymysql.connect(user='',
                     password='',
                     host='',
                     cursorclass=pymysql.cursors.DictCursor)
# Enter user, password and host. Deleted for security purposes
cursor = db.cursor()

count = 0
@application.route("/")
def home():
    global count
    count = count + 1
    pagetime = datetime.datetime.now()
    return render_template('home.html', count=count, pagetime=pagetime)


@application.route("/check", methods=["POST", "GET"])
def check():
    fname = request.form['fname']
    lname = request.form['lname']

    start_time = time.time()

    sql1 = "SELECT * FROM dbo.student WHERE fname = '" + str(fname) + "' AND lname = '" + str(lname) + "'"
    cursor.execute(sql1)
    rows1 = cursor.fetchall()

    if rows1 is None:
        age = request.form['age']
        credit = request.form['credit']
        idnum = request.form['idnum']
        val = (idnum, fname, lname, age)

        sql2 = "INSERT INTO dbo.student (`idnum`, `fname`, `lname`, `age`, `credit`) VALUES (%s,%s,%s,%s,20)"
        cursor.execute(sql2, val)

    course = int(request.form['course'])
    section = int(request.form['section'])

    sql3 = "SELECT * FROM dbo.stco"
    cursor.execute(sql3)
    rows3 = cursor.fetchall()

    sql4 = "SELECT * FROM dbo.course WHERE maxseats <> 0"
    cursor.execute(sql4)
    rows4 = cursor.fetchall()

    sql5 = "SELECT * FROM dbo.course WHERE course= '" + str(course) + "' AND section= '" + str(section) + "' AND  maxseats <> 0"
    cursor.execute(sql5)
    rows5 = cursor.fetchall()

    val1 = (course, section, fname, lname)

    if rows5 is not None:
        sql6 = "UPDATE dbo.course SET maxseats = maxseats-1 WHERE course = '" + str(course) + "' AND section = '" + str(section) + "'"
        cursor.execute(sql6)
        sql61 = "UPDATE dbo.student SET credit = credit-20 WHERE fname = '" + str(fname) + "' AND lname = '" + str(lname) + "'"
        cursor.execute(sql61)
        sql7 = "INSERT INTO dbo.stco (`course`, `section`, `fname`, `lname`) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql7, val1)

    sql6 = "SELECT maxseats FROM dbo.course WHERE course = '" + str(course) + "' AND section = '" + str(section) + "'"
    cursor.execute(sql6)
    rows6 = cursor.fetchall()

    sql8 = "SELECT * FROM dbo.stco"
    cursor.execute(sql8)
    rows8 = cursor.fetchall()

    sql9 = "SELECT * FROM dbo.student"
    cursor.execute(sql9)
    rows9 = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time-start_time

    return render_template("check.html", elapsed_time=elapsed_time, rows1=rows1,rows3=rows3, rows4=rows4, rows5=rows5, rows6=rows6, rows8=rows8, rows9=rows9)


    # return render_template("check.html", elapsed_time=elapsed_time, rows3=rows3, rows4=rows4, rows5=rows5, rows6=rows6, rows8=rows8, rows9=rows9)


# @application.route("/update", methods=["POST", "GET"])
# def update():
#     start_time = time.time()
#
#     sql1 = "SELECT * FROM dbo.stco"
#     cursor.execute(sql1)
#     rows1 = cursor.fetchall()
#
#     sql2 = "SELECT * FROM dbo.course WHERE maxseats <> 0"
#     cursor.execute(sql2)
#     rows2 = cursor.fetchall()
#
#     course = int(request.form['course'])
#     section = int(request.form['section'])
#
#     sql3 = "SELECT * FROM dbo.course WHERE course= '" + str(course) + "' AND section= '" + str(section) + "' AND  maxseats <> 0"
#     cursor.execute(sql3)
#     rows3 = cursor.fetchall()
#
#     if rows3 is not None:
#         sql4 = "UPDATE dbo.course SET maxseats = maxseats-1 WHERE course = '" + str(course) + "' AND section = '" + str(section) + "'"
#         cursor.execute(sql4)
#         # sql5 = "INSERT INTO dbo.stco(course, section) VALUES ('" + str(course) + "', '" + str(section) + "')"
#         # cursor.execute(sql5)
#
#     sql6 = "SELECT maxseats FROM dbo.course WHERE course = '" + str(course) + "' AND section = '" + str(section) + "'"
#     cursor.execute(sql6)
#     rows6 = cursor.fetchall()
#
#     sql8 = "SELECT * FROM dbo.stco"
#     cursor.execute(sql8)
#     rows8 = cursor.fetchall()
#
#     sql9 = "SELECT sc.sid, sc.course, sc.section, c.maxseats FROM dbo.st as s, dbo.cr as c, dbo.stco as sc WHERE sc.sid=s.idnum AND sc.course=c.course AND sc.section=c.section"
#     cursor.execute(sql9)
#     rows9 = cursor.fetchall()
#
#     end_time = time.time()
#     elapsed_time = end_time-start_time
#
#     return render_template("update.html", rows1=rows1, rows2=rows2, rows6=rows6, rows8=rows8, rows9=rows9, elapsed_time=elapsed_time)


if __name__ == "__main__":
    application.debug = True
    application.run()