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
    total2 = 0
    no = int(request.form.get('no', ''))
    query2 = "SELECT * FROM earth WHERE mag=3.3"
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


@app.route('/restqueries', methods=['POST', 'GET'])
def restqueries():

    n = int(request.form.get('n', ''))
    mag1 = float(request.form.get('m1', ''))
    mag2 = float(request.form.get('m2', ''))
    total3 = 0

    start3 = time.time()
    for i in range(0, n):
        val = random.uniform(mag1, mag2)
        magval = round(val, 2)
        query3 = "SELECT * FROM earth WHERE mag = '" + str(magval) + "'"
        hash1 = hashlib.sha256(query3.encode()).hexdigest()

        if r.get(hash1):
            print("This was return from redis")
        else:
            cursor.execute(query3)
            t3 = cursor.fetchall()
            rows1 = []
            for x in t3:
                rows1.append(str(x))
                r.set(hash1, pickle.dumps(list(rows1)))
                r.expire(hash1, 36)
                print("This is the cached data")
    end3 = time.time()
    total3 = (end3-start3)
    avg3 = (total3/n)
    print('hi2')

    total33 = 0

    for number in range(0, n):
        start33 = time.time()
        cursor.execdirect(query3)
        t33 = cursor.fetchall()
        end33 = time.time()
        total33 = (end33 - start33) + total33
    avg33 = (total33 / n)
    print('hi22')

    return render_template('restqueries.html', times3=n, totaltime3=total3, avgtime3=avg3, totaltime33=total33,
                           avgtime33=avg33)


@app.route('/restqueries2', methods=['POST', 'GET'])
def restqueries2():
    n2 = int(request.form.get('n2', ''))
    mg1 = float(request.form.get('mg1', ''))
    mg2 = float(request.form.get('mg2', ''))
    total4 = 0

    start4 = time.time()
    for i in range(0, n2):
        val = random.uniform(mg1, mg2)
        magval = round(val, 2)
        query4 = "SELECT * FROM earth WHERE mag = '"+str(magval)+"' AND locsrc='ak'"
        hash2 = hashlib.sha256(query4.encode()).hexdigest()

        if r.get(hash2):
            print("This was return from redis")
        else:
            cursor.execute(query4)
            t4 = cursor.fetchall()
            rows1 = []
            for x in t4:
                rows1.append(str(x))
                r.set(hash2, pickle.dumps(list(rows1)))
                r.expire(hash2, 36)
                print("This is the cached data")
    end4 = time.time()
    total4 = (end4 - start4)
    avg4 = (total4 / n2)
    print('hi2')

    total44 = 0
    for number in range(0, n2):
        start44 = time.time()
        query4 = "SELECT * FROM earth WHERE mag = '"+str(magval)+"' AND locsrc='ak'"
        cursor.execdirect(query4)
        t44 = cursor.fetchall()
        end44 = time.time()
        total44 = (end44-start44)+total44
    avg44 = (total44/n2)
    print('hi2')

    return render_template('restqueries2.html', times4=n2,
                           totaltime4=total4, avgtime4=avg4, totaltime44=total44, avgtime44=avg44)


if __name__ == '__main__':
  app.run()
