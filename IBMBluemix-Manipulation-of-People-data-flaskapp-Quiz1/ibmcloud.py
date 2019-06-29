import os
from flask import Flask, redirect, render_template, request
import json
import ibm_db
# from flask_db2 import DB2

app = Flask(__name__, static_url_path='')

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=;PORT=50000;PROTOCOL=TCPIP;UID=;PWD=;", "", "")
print("Connected to db")  # Enter the host name userid and password---deleted for security purposes
# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
    db2cred = db2info["credentials"]

else:
    raise ValueError('Expected cloud environment')

@app.route("/", methods=["POST", "GET"])
def getdata():
    listofdata = []
    query1 = "SELECT * FROM QPEOPLE"
    stmt = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt)
    while result:
        listofdata.append(result)
        result = ibm_db.fetch_both(stmt)

    return render_template('main.html', table=listofdata)


@app.route("/display", methods=["POST", "GET"])
def display():
    # name = request.form.get("name")
    kword_data = []
    query1 = "SELECT NAME,PICTURE FROM QPEOPLE"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        kword_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('display.html', table=kword_data, title='Display')

@app.route("/showpoint", methods=["POST", "GET"])
def showpoint():
    point = request.form.get("point")
    point_data = []
    query1 = "SELECT NAME,PICTURE,FAVORITE FROM QPEOPLE WHERE POINTS = '"+ str(point)+ "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        point_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('showpoint.html', table=point_data, title='Show point')

@app.route("/word", methods=["POST", "GET"])
def word():
    range1 = request.form.get("range1")
    range2 = request.form.get("range2")
    word = request.form.get("word")

    all_data = []
    query1 = "SELECT NAME,STATE,PICTURE FROM QPEOPLE WHERE FAVORITE LIKE '%"+ str(word)+ "%' AND POINTS BETWEEN '"+ str(range1)+ "' AND '"+ str(range2)+ "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        all_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('word.html', table=all_data, title='Word')


@app.route("/update", methods=["POST", "GET"])
def update():
    point = request.form.get("point")
    name = request.form.get("name")
    cpoint = request.form.get("cpoint")
    favorite = request.form.get("favorite")
    kword_data = []
    if cpoint:
        query1 = "UPDATE QPEOPLE SET POINTS = '" + str(cpoint) + "' WHERE POINTS = '"+ str(point)+ "'"
    elif name:
        query1 = "UPDATE QPEOPLE SET NAME = '" + str(name) + "' WHERE POINTS = '"+ str(point)+ "'"
    elif favorite:
        query1 = "UPDATE QPEOPLE SET FAVORITE = '" + str(favorite) + "' WHERE POINTS = '"+ str(point)+ "'"
    else:
        pass
    
    stmt1 = ibm_db.exec_immediate(conn, query1)
    query2 = "SELECT * FROM QPEOPLE"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result = ibm_db.fetch_both(stmt2)
    while result:
        kword_data.append(result)
        result = ibm_db.fetch_both(stmt2)

    return render_template('update.html', table=kword_data, title='Update')


# @app.route("/")
# @app.route("/main")
# @app.route("/home")
# def main():
#     # return render_template('main.html', listofdata=listofdata, title='Home')
#     return render_template('main.html', title='Home')

port = os.getenv('PORT', '5000')

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=int(port))
    app.run(host='0.0.0.0', port=int(port))
