import pypyodbc
from flask import Flask, request, render_template
import sys
import json
from json import loads, dumps

app = Flask(__name__)

conn = pypyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        'SERVER=;'
                        'PORT=1443;'
                        'DATABASE=mydb1;'
                        'UID=;'
                        'PWD=')
# Enter Server, UID and PWD. Deleted for security purposes
cursor = conn.cursor()


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/list", methods=["POST", "GET"])
def list():
    # depthrange1 = float(request.form.get('depthrange1', ''))
    # query1="SELECT * FROM earthq WHERE latitude >= '" + str(latitude1) + "' AND latitude <= '" + str(latitude2) + "' AND longitude >= '" + str(longitude1) + "' AND longitude <= '" + str(longitude2) + "'"


    query1 = "select * from voting where totalpop between 2000 and 8000"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "select * from voting where totalpop between 8000 and 40000"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    return render_template('list.html', rows1=r1, rows2=r2)


@app.route("/showpie", methods=["POST", "GET"])
def showpie():

    range1 = 0
    range2 = int(request.form.get('range2', ''))

    query1 = "SELECT max(totalpop) FROM voting"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    totrange = 0
    count = 0
    range11 = []


    for i in range(range2):
        if (totrange <= r1[0][0]):
            totrange += range2
        if totrange> r1[0][0]:
            break

        query2 = "SELECT count(*) FROM voting WHERE totalpop between '" + str(range1) + "' AND '" + str(range2) + "'"
        cursor.execute(query2)
        r2 = cursor.fetchall()
        range1 = range2
        range2 = range1 + totrange
        count = count + 1
        range11.append(range1)

    range11.append(range2)


    rows = ([
        ['State', 'Number of population'],
        [str(range11[0][0]) + '-' + str(range1[0][1]), r2[0][0]],
        [str(range11[0][2]) + '-' + str(range1[0][3]), r2[0][0]],
        [str(range11[0][4]) + '-' + str(range1[0][5]), r2[0][0]],
        [str(range11[0][6]) + '-' + str(range1[0][7]), r2[0][0]],
        [str(range11[0][8]) + '-' + str(range1[0][9]), r2[0][0]]

    ])

    return render_template('showpie.html', rows=rows)


@app.route("/bar", methods=["POST", "GET"])
def bar():

    r1 = []
    range1 = int(request.form.get('range', ''))

    for i in range(range1):
        modulo = (i**3)%10
        r1.append(modulo)


    rows=([
        ['Modulo', 'Number'],
        ['0', r1[0]],
        ['1', r1[0]],
        ['2', r1[0]],
        ['3', r1[0]],
        ['4', r1[0]],
        ['5', r1[0]],
        ['6', r1[0]],
        ['7', r1[0]],
        ['8', r1[0]],
        ['9', r1[0]]

    ])

    return render_template('bar.html', rows=rows)

@app.route("/scatter", methods=["POST", "GET"])
def scatter():
    range1 = int(request.form.get('range1', ''))
    range2 = int(request.form.get('range2', ''))


    query1 = "SELECT count(state) FROM voting WHERE totalpop between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()


    rows = ([
        ['Population', 'State'],
        [str(range1) + '-' + str(range2), r1[0][0]]
    ])

    return render_template('scatter.html', rows=rows)


@app.route("/line", methods=["POST", "GET"])
def line():
    locationsrc = str(request.form.get('locationsrc', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM earthq WHERE locationsrc = '" + str(locationsrc) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM earthq WHERE locationsrc = '" + str(locationsrc) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM earthq WHERE locationsrc = '" + str(locationsrc) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of Earthquakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    return render_template('line.html', rows=rows)


if __name__ == '__main__':
    app.run()
