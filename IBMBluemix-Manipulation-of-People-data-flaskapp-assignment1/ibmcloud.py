import os
from flask import Flask, redirect, render_template, request
import json
import ibm_db
# from flask_db2 import DB2

app = Flask(__name__, static_url_path='')

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=;PORT=50000;PROTOCOL=TCPIP;UID=;PWD=;", "", "")
print("Connected to db") # Enter the host name userid and password---deleted for security purposes
# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
    db2cred = db2info["credentials"]

else:
    raise ValueError('Expected cloud environment')

@app.route("/", methods=["POST", "GET"])
def getdata():
    listofdata = []
    query1 = "SELECT * FROM PEOPLE"
    stmt = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt)
    while result:
        listofdata.append(result)
        result = ibm_db.fetch_both(stmt)

    return render_template('main.html', table=listofdata)


@app.route("/update", methods=["POST", "GET"])
def update():
    kword = request.form.get("keywords")
    pid = request.form.get("pid")
    kword_data = []
    query1 = "UPDATE PEOPLE SET KEYWORDS = '" + str(kword) + "' WHERE ID = '"+ str(pid)+ "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    print("update: ", stmt1)
    query2 = "SELECT * FROM PEOPLE"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result = ibm_db.fetch_both(stmt2)
    while result:
        kword_data.append(result)
        result = ibm_db.fetch_both(stmt2)

    return render_template('update.html', table=kword_data, title='Update')

@app.route("/show", methods=["POST", "GET"])
def show():
    name = request.form.get("name")
    query1 = "SELECT PICTURE FROM PEOPLE WHERE NAME = '" + str(name) + "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        photo = result[0]
        result = ibm_db.fetch_both(stmt1)

    return render_template('show.html', filename=photo, name=name, title='Show')

@app.route("/insert", methods=["POST", "GET"])
def insert():
    pid = request.form.get("pid")
    file = request.form['file']
    query1 = "UPDATE PEOPLE SET PICTURE = '" + str(file) + "' WHERE ID = '" + str(pid) + "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    print(stmt1)

    return render_template('insert.html', filename=file, title='Add/Insert')


@app.route("/delete", methods=["POST", "GET"])
def delete():
    dname = request.form.get("dname")
    pid = request.form.get("pid")
    deleted_data = []
    query1 = "DELETE FROM PEOPLE WHERE ID = '" + str(pid) + "' AND NAME = '" + str(dname)+"'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    # result = ibm_db.fetch_both(stmt1)
    query2 = "SELECT * FROM PEOPLE"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result = ibm_db.fetch_both(stmt2)
    while result:
        deleted_data.append(result)
        result = ibm_db.fetch_both(stmt2)

    return render_template('delete.html', table=deleted_data, title='Delete')


@app.route("/withinrange", methods=["POST", "GET"])
def withinrange():
    range1 = request.form.get("range1")
    range2 = request.form.get("range2")
    range_data = []
    query1 = "SELECT * FROM PEOPLE WHERE SALARY BETWEEN '" + str(range1) + "' AND '" + str(range2)+"'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        range_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('withinrange.html', table=range_data, title='Within Range')


@app.route("/greaterthan", methods=["POST", "GET"])
def greaterthan():
    range1 = request.form.get("range1")
    # range2 = request.form.get("range2")
    greater_data = []
    query1 = "SELECT * FROM PEOPLE WHERE SALARY > '" + str(range1) + "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        greater_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('greaterthan.html', table=greater_data, title='Greater Than')


@app.route("/lessthan", methods=["POST", "GET"])
def lessthan():
    range1 = request.form.get("range1")
    # range2 = request.form.get("range2")
    less_data = []
    query1 = "SELECT * FROM PEOPLE WHERE SALARY < '" + str(range1) + "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        less_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('lessthan.html', table=less_data, title='Less Than')

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
