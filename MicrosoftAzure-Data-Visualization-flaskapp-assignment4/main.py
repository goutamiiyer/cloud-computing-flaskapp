import pypyodbc
from flask import Flask, request, render_template
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
    locationsrc = str(request.form.get('locationsrc', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM earthq WHERE locationsrc = '" + str(locationsrc) + "' AND mag between '" + str(range1) + "' AND '" + str(range2) + "'"
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
    return render_template('list.html', rows1=r1, rows2=r2, rows3=r3)


@app.route("/showpie", methods=["POST", "GET"])
def showpie():
    locationsrc = str(request.form.get('locationsrc', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM earthq WHERE locationsrc = '" + str(locationsrc) + "' AND mag between '" + str(range1) + "' AND '" + str(range2) + "'"
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
        ['Magnitude', 'Number of quakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]

    ])

    return render_template('showpie.html', rows=rows)


@app.route("/pie", methods=["POST", "GET"])
def pie():
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

    rows1 = ([
        ['Magnitude', 'Number of Earthquakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    query8 = "select count(*) from earthq where mag > 5.0 and deptherror > 5"
    cursor.execute(query8)
    r8 = cursor.fetchall()
    query9 = "select count(*) from earthq where mag > 5.0 and deptherror < 5"
    cursor.execute(query9)
    r9 = cursor.fetchall()

    rows2 = ([
        ['Magnitude and Depth Error', 'Number of Earthquakes'],
        ['Depth Error > 5', r8[0][0]],
        ['Depth Error < 5', r9[0][0]]

    ])

    return render_template('pie.html', rows=[rows1, rows2])


@app.route("/bar", methods=["POST", "GET"])
def bar():
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

    return render_template('bar.html', rows=rows)

@app.route("/scatter", methods=["POST", "GET"])
def scatter():
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
