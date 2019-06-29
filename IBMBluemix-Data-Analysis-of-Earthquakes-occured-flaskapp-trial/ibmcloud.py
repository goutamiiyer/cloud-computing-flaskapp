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
    query1 = "SELECT * FROM EARTHQ LIMIT 20"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        upload_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('upload.html', table=upload_data, rowcount=len(upload_data), title='Upload data')


@app.route("/range", methods=["POST", "GET"])
def range():
    range1 = request.form.get("magrange1")
    range2 = request.form.get("magrange2")
    
    inside_range_data = []
    # query1 = "SELECT * FROM EARTHQ WITH(INDEX(EARTHQIND)) WHERE MAG BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
    query1 = "SELECT COUNT(*) FROM EARTHQ WHERE MAG BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        inside_range_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    below_range_data = []
    query2 = "SELECT COUNT(*) FROM EARTHQ WHERE MAG BETWEEN '0' AND '" + str(range1) + "'"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result2 = ibm_db.fetch_both(stmt2)
    while result2:
        below_range_data.append(result2)
        result2 = ibm_db.fetch_both(stmt2)

    above_range_data = []
    query3 = "SELECT COUNT(*) FROM EARTHQ WHERE MAG BETWEEN '" + str(range2) + "' AND (SELECT MAX(MAG) FROM EARTHQ)"
    stmt3 = ibm_db.exec_immediate(conn, query3)
    result3 = ibm_db.fetch_both(stmt3)
    while result3:
        above_range_data.append(result3)
        result3 = ibm_db.fetch_both(stmt3)

    return render_template('range.html', table=inside_range_data, below = below_range_data, above = above_range_data, rowcount=len(inside_range_data), rowabove=len(above_range_data), rowbelow=len(below_range_data), title='Greater Than')


@app.route("/locationsource", methods=["POST", "GET"])
def locationsource():
    locationsource = request.form.get("locationsource")
    magnitude = request.form.get("mag")
    
    locationsource_data = []
    query1 = "SELECT * FROM EARTHQ WHERE MAG > '" + str(magnitude) + "' AND LOCATIONSOURCE = '" + str(locationsource) + "' AND ((MAGNST*2) >= NST)"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        locationsource_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('locationsource.html', table=locationsource_data, rowcount=len(locationsource_data), title='Location Source')



port = os.getenv('PORT', '5000')

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=int(port))
    app.run(host='0.0.0.0', port=int(port))
