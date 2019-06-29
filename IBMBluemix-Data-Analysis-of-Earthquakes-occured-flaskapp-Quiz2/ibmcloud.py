import os
from flask import Flask, redirect, render_template, request
import json
import ibm_db
from math import radians, cos, sin, asin, sqrt, atan2
import pandas as pd
import sqlite3

# from flask_db2 import DB2

app = Flask(__name__, static_url_path='')

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=xff76659;PWD=whk3f@vmfrnx00dl;", "", "")
print("Connected to db")
# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
    db2cred = db2info["credentials"]

else:
    raise ValueError('Expected cloud environment')

@app.route("/", methods=["POST", "GET"])
def getdata():
    listofdata = []
    # query1 = "SELECT * FROM EARTHQ LIMIT 5"
    # stmt = ibm_db.exec_immediate(conn, query1)
    # result = ibm_db.fetch_both(stmt)
    # while result:
    #     listofdata.append(result)
    #     result = ibm_db.fetch_both(stmt)

    return render_template('main.html', table=listofdata)


@app.route("/upload", methods=["POST", "GET"])
def upload():
    # if request.method == 'POST':
    #     con = sql.connect("database.db")
    #     csv = request.files['myfile']
    #     file = pd.read_csv(csv)
    #     file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
    #     con.close()
    
    
    upload_data = []
    query1 = "SELECT COUNT(*) AS TOTAL, MIN(MAG) AS MINMAG, PLACE, LATITUDE, LONGITUDE FROM EARTHQ GROUP BY LATITUDE,LONGITUDE,PLACE HAVING MIN(MAG) > '2'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        upload_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('upload.html', table=upload_data, rowcount=len(upload_data), title='Upload data')


@app.route("/range", methods=["POST", "GET"])
def range():
    range1 = request.form.get("depthrange1")
    range2 = request.form.get("depthrange2")
    increment = int(request.form.get("increment"))


    range_data = []
    count = int(range2)

    while (count-int(range1) != 0):
        query1 = "SELECT COUNT(*) FROM EARTHQ WHERE DEPTH BETWEEN '" + str(range1) + "' AND '" + str(count) + "'"
        stmt1 = ibm_db.exec_immediate(conn, query1)
        result = ibm_db.fetch_both(stmt1)
        while result:
            range_data.append(result)
            result = ibm_db.fetch_both(stmt1)

        count = count - increment

    return render_template('range.html', table=range_data, title='Range data')


@app.route("/update", methods=["POST", "GET"])
def update():
    depthrange1 = request.form.get("depthrange1")
    depthrange2 = request.form.get("depthrange2")
    startdate = request.form.get("startdate")
    enddate = request.form.get("enddate")
    magnitude = request.form.get("mag")

    
    update_data = []
    query1 = "UPDATE EARTHQ SET MAG = '" + str(magnitude) + "'  WHERE DEPTH BETWEEN '" + str(depthrange1) + "' AND '" + str(depthrange2) + "' AND GMTTIME BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    # result = ibm_db.fetch_both(stmt1)
    query2 = "SELECT * FROM EARTHQ  WHERE DEPTH BETWEEN '" + str(depthrange1) + "' AND '" + str(depthrange2) + "' AND GMTTIME BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result = ibm_db.fetch_both(stmt2)
    while result:
        update_data.append(result)
        result = ibm_db.fetch_both(stmt2)

    return render_template('update.html', table=update_data, rowcount=len(update_data), title='Update Data')



port = os.getenv('PORT', '5000')

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=int(port))
    app.run(host='0.0.0.0', port=int(port))
