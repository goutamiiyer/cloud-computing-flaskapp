import pypyodbc
from flask import Flask, request, render_template
from random import randint
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
    rms = float(request.form.get('rms', ''))
    query1 = "SELECT * FROM EARTHQ WHERE RMS > '" + str(rms) + "'"
    start_time = time.time()
    cursor.execute(query1)
    rows = cursor.fetchall()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template('display.html', table=rows, rowcount=len(rows), elapsed_time=elapsed_time)


@app.route("/listofqueries", methods=["POST", "GET"])
def listofqueries():
    magrange1 = float(request.form.get('magrange1', ''))
    magrange2 = float(request.form.get('magrange2', ''))
    query1 = "SELECT * FROM EARTHQ WHERE MAG BETWEEN '" + str(magrange1) + "' AND '" + str(magrange2) + "'"
    start_time = time.time()
    cursor.execute(query1)
    rows = cursor.fetchall()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template('listofqueries.html', table=rows, rowcount=len(rows), elapsed_time=elapsed_time)


@app.route("/queries", methods=["POST", "GET"])
def queries():
    # net = request.form.get('net', '')
    # mag = float(request.form.get('mag', ''))
    # query1 = "SELECT * FROM EARTHQ WHERE NET LIKE '%" + str(net) + "%'"

    num = int(request.form.get('num', ''))

    sql_query_list = []

    sql1 = "SELECT latitude FROM earthq where locationsrc='ak'"
    sql_query_list.append(sql1)
    sql2 = "SELECT latitude FROM earthq where locationsrc='hv'"
    sql_query_list.append(sql2)
    sql3 = "SELECT latitude FROM earthq where locationsrc='ak'"
    sql_query_list.append(sql3)
    lensqllist = len(sql_query_list)

    start_time = time.time()

    for i in range(1,int(num)):
        randid = randint(1, int(lensqllist) - 1)
        sqlquery = sql_query_list[int(randid)]
        cursor.execute(sqlquery)
        rows = cursor.fetchall()

    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template('queries.html', rowcount=len(rows), elapsed_time=elapsed_time)


@app.route("/restricted", methods=["POST", "GET"])
def restricted():
    num = int(request.form.get('num', ''))
    start_time = time.time()

    for i in range(1, int(num)):
        randid = randint(100, 300)
        query3 = "SELECT latitude, longitude, depth, mag FROM earthq WHERE LATITUDE = " + "'" + str(randid) +"'"

        queryhash = hashlib.sha256(query3).hexdigest()
        result = r.get(queryhash)

        if not result:
            cursor.execute(query3)
            result = cursor.fetchall()
            r.set(queryhash, result)

    end_time = time.time()
    elapsed_time = end_time - start_time

    return render_template('restricted.html', elapsed_time=elapsed_time)


@app.route('/noqueries', methods=['POST', 'GET'])
def noqueries():
    totaltime = 0

    times = int(request.form.get('times', ''))

    query1 = "SELECT * FROM earth WHERE mag=3.3"

    start = time.time()

    for i in range(0, times):
        hash1 = hashlib.sha256(query1.encode()).hexdigest()

        if r.get(hash1):
            print("This was return from redis")
        else:
            cursor.execute(query1)
            t1 = cursor.fetchall()
            rows1 = []

            for x in t1:
                rows1.append(str(x))
                r.set(hash1, pickle.dumps(list(rows1)))
                r.expire(hash1, 36)
                print("This is the cached data")

    end = time.time()
    totaltime = (end - start)
    avg = (totaltime / times)

    elapsed_time = 0

    for number in range(0, times):
        start_time = time.time()

        cursor.execdirect(query1)
        t12 = cursor.fetchall()

        end_time = time.time()
        elapsed_time = (end_time - start_time) + elapsed_time

    avg_time = (elapsed_time / times)

    return render_template('noqueries.html', times=times, totaltime=totaltime, avgtime=avg, elapsed_time=elapsed_time,
                           avg_time=avg_time)


@app.route('/restrictquery', methods=['POST', 'GET'])
def restrictquery():

    times = int(request.form.get('times', ''))
    mag1 = float(request.form.get('m1', ''))
    mag2 = float(request.form.get('m2', ''))

    totaltime = 0

    start = time.time()

    for i in range(0, times):
        val = random.uniform(mag1, mag2)
        magval = round(val, 2)

        query1 = "SELECT * FROM earth WHERE mag = '" + str(magval) + "'"
        hash1 = hashlib.sha256(query1.encode()).hexdigest()

        if r.get(hash1):
            print("This was return from redis")
        else:
            cursor.execute(query1)
            t1 = cursor.fetchall()
            rows1 = []
            for x in t1:
                rows1.append(str(x))
                r.set(hash1, pickle.dumps(list(rows1)))
                r.expire(hash1, 36)
                print("This is the cached data")

    end = time.time()
    totaltime = (end-start)
    avg = (totaltime/times)

    elapsed_time = 0

    for number in range(0, times):
        start_time = time.time()
        cursor.execdirect(query1)
        t12 = cursor.fetchall()
        end_time = time.time()
        elapsed_time = (end_time - start_time) + elapsed_time
    avg_time = (elapsed_time / times)

    return render_template('restrictquery.html', times=times, totaltime=totaltime, avgtime=avg, elapsed_time=elapsed_time,
                           avg_time=avg_time)


@app.route('/restquery', methods=['POST', 'GET'])
def restquery():
    times = int(request.form.get('times', ''))
    mg1 = float(request.form.get('mg1', ''))
    mg2 = float(request.form.get('mg2', ''))

    totaltime = 0

    start = time.time()

    for i in range(0, times):
        val = random.uniform(mg1, mg2)
        magval = round(val, 2)

        query1 = "SELECT * FROM earth WHERE mag = '"+str(magval)+"' AND locsrc='us'"
        hash1 = hashlib.sha256(query1.encode()).hexdigest()

        if r.get(hash1):
            print("This was return from redis")
        else:
            cursor.execute(query1)
            t1 = cursor.fetchall()
            rows1 = []
            for x in t1:
                rows1.append(str(x))
                r.set(hash1, pickle.dumps(list(rows1)))
                r.expire(hash1, 36)
                print("This is the cached data")

    end = time.time()
    totaltime = (end - start)
    avg = (totaltime / times)

    elapsed_time = 0

    for number in range(0, times):
        start_time = time.time()

        query1 = "SELECT * FROM earth WHERE mag = '"+str(magval)+"' AND locsrc='us'"
        cursor.execdirect(query1)
        t12 = cursor.fetchall()

        end_time = time.time()
        elapsed_time = (end_time-start_time)+elapsed_time

    avg_time = (elapsed_time/times)

    return render_template('restquery.html', times=times,
                           totaltime=totaltime, avgtime=avg, elapsed_time=elapsed_time, avg_time=avg_time)


if __name__ == '__main__':
  app.run()
