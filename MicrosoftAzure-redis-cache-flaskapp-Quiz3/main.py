import pypyodbc
from flask import Flask, request, render_template
from random import randrange
import random
import time
import redis
import hashlib
import pickle
from datetime import datetime
from json import loads, dumps

app = Flask(__name__)

cache = 'c1'

r = redis.StrictRedis(
    host='',
    port=6380,
    password='', ssl=True)
# Enter Server, host and password. Deleted for security purposes

list1 = []
list2 = []

conn = pypyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        'SERVER=;'
                        'PORT=1443;'
                        'DATABASE=mydb1;'
                        'UID=;'
                        'PWD=')
# Enter Server, UID and PWD. Deleted for security purposes
cursor = conn.cursor()


@app.route('/')
def my_form():
    query = "SELECT MIN(MAG) FROM EARTHQ"
    cursor.execute(query)
    rows = cursor.fetchall()
    return render_template('my-form.html', single=rows[0])


@app.route("/display", methods=["POST", "GET"])
def display():
    depthrange1 = float(request.form.get('depthrange1', ''))
    depthrange2 = float(request.form.get('depthrange2', ''))
    longitude = float(request.form.get('longitude', ''))

    query1 = "SELECT latitude, longitude, gmt, deptherror FROM quakes WHERE longitude > '" + str(longitude) + "' AND deptherror BETWEEN '" + str(depthrange1) + "' AND '" + str(depthrange2) + "'"
    start_time = time.time()
    cursor.execute(query1)
    rows = cursor.fetchall()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template('display.html', table=rows, rowcount=len(rows), elapsed_time=elapsed_time)


@app.route("/random", methods=["POST", "GET"])
def random():
    num = int(request.form.get('num', ''))
    range1 = float(request.form.get('depthrange1', ''))
    range2 = float(request.form.get('depthrange2', ''))

    rand1=[]
    rand2=[]
    timediff=[]
    getrows =[]

    start_time = time.time()

    for i in range(1, int(num)):
        randid1 = randrange(range1,range2)
        rand1.append(randid1)
        randid2 = randrange(range1,range2)
        rand2.append(randid2)
        query1 = "SELECT latitude, longitude, gmt, deptherror FROM quakes WHERE deptherror BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
        cursor.execute(query1)
        rows = cursor.fetchall()
        rowlen = len(rows)
        getrows.append(rowlen)
        end_time = time.time()
        elapsed_time = end_time - start_time
        timediff.append(elapsed_time)
    return render_template('random.html', times=num, table=rows, rowcount=getrows, timediff=timediff,
                           rand1=rand1, rand2=rand2)



@app.route("/cumulative", methods=["POST", "GET"])
def cumulative():
    num = int(request.form.get('num', ''))
    range1 = float(request.form.get('depthrange1', ''))
    range2 = float(request.form.get('depthrange2', ''))

    rand1=[]
    rand2=[]
    timediff=[]
    getrows =[]

    start_time = time.time()

    for i in range(1, int(num)):
        randid1 = randrange(range1,range2)
        rand1.append(randid1)
        randid2 = randrange(range1,range2)
        rand2.append(randid2)
        query1 = "SELECT latitude, longitude, gmt, deptherror FROM quakes WHERE deptherror BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
        cursor.execute(query1)
        rows = cursor.fetchall()
        rowlen = len(rows)
        getrows.append(rowlen)
        end_time = time.time()
        elapsed_time = end_time - start_time
        timediff.append(elapsed_time)

    end_time1 = time.time()
    timed = end_time1-start_time
    return render_template('cumulative.html', times=num, table=rows, rowcount=getrows, timediff=timediff,
                           rand1=rand1, rand2=rand2, timed=timed)


@app.route('/noqueries', methods=['POST', 'GET'])
def noqueries():
    range1 = float(request.form.get('depthrange1', ''))
    range2 = float(request.form.get('depthrange2', ''))

    total2 = 0
    no = int(request.form.get('num', ''))
    query2 = "SELECT latitude, longitude, gmt, deptherror FROM quakes WHERE deptherror BETWEEN '" + str(
        range1) + "' AND '" + str(range2) + "'"
    start2 = time.time()

    for i in range(0, no):
        hash1 = hashlib.sha256(query2.encode()).hexdigest()

        if r.get(hash1):
            print("This was return from redis")
        else:
            cursor.execute(query2)
            t2 = cursor.fetchall()
            rows1 = []
            for x in t2:
                rows1.append(str(x))
                r.set(hash1, pickle.dumps(list(rows1)))
                r.expire(hash1, 36)
                print("This is the cached data")
    end2 = time.time()
    total2 = (end2 - start2)
    avg2 = (total2 / no)
    print('hi2')

    total22 = 0

    for number in range(0, no):
        start22 = time.time()
        cursor.execdirect(query2)
        t22 = cursor.fetchall()
        end22 = time.time()
        total22 = (end22 - start22) + total22
    avg22 = (total22 / no)
    print('hi22')

    return render_template('noqueries.html', times=no, totaltime=total2, avgtime=avg2, totaltime22=total22,
                           avgtime22=avg22)


if __name__ == '__main__':
  app.run()
