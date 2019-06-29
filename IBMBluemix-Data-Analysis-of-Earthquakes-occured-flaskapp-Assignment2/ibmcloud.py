import os
from flask import Flask, redirect, render_template, request
import json
import ibm_db
from math import radians, cos, sin, asin, sqrt, atan2

# from flask_db2 import DB2

app = Flask(__name__, static_url_path='')

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=;PORT=50000;PROTOCOL=TCPIP;UID=;PWD=;", "", "")
print("Connected to db")    # Enter the host name userid and password---deleted for security purposes
# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
    db2cred = db2info["credentials"]

else:
    raise ValueError('Expected cloud environment')

@app.route("/", methods=["POST", "GET"])
def getdata():
    listofdata = []
    query1 = "SELECT * FROM EARTHQ LIMIT 5"
    stmt = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt)
    while result:
        listofdata.append(result)
        result = ibm_db.fetch_both(stmt)

    return render_template('main.html', table=listofdata)


@app.route("/greaterthan", methods=["POST", "GET"])
def greaterthan():
    range1 = request.form.get("range1")
    
    greater_data = []
    query1 = "SELECT * FROM EARTHQ WHERE MAG > '" + str(range1) + "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        greater_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('greaterthan.html', table=greater_data, rowcount=len(greater_data), title='Greater Than')


@app.route("/withinrange", methods=["POST", "GET"])
def withinrange():
    range1 = request.form.get("magrange1")
    range2 = request.form.get("magrange2")
    startdate = request.form.get("startdate")
    enddate = request.form.get("enddate")
    
    range_data = []
    query1 = "SELECT * FROM EARTHQ WHERE MAG BETWEEN '" + str(range1) + "' AND '" + str(range2) + "' AND GMTTIME BETWEEN '" + str(startdate) + "%' AND '" + str(enddate) + "%'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        range_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('withinrange.html', table=range_data, rowcount=len(range_data), title='Within Range')


@app.route("/locationdist", methods=["POST", "GET"])
def locationdist():

    query1 = "SELECT * FROM EARTHQ"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    results = ibm_db.fetch_both(stmt1)

    R = 6373.0

    lat1 = radians(float(request.form.get("latitude")))
    lon1 = radians(float(request.form.get("longitude")))
    
    locationdist_data = []

    for result in results:
        lat2 = radians(float(result[2]))
        lon2 = radians(float(result[3]))
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance =float(R * c)
        if distance <= (float(request.form['distance'])):
            locationdist_data.append(result)

    # query2 ='SELECT * FROM (select *,(((acos(sin(('+lat1+'*3.14/180)) * sin(("latitude"*3.14/180))+cos(('+lat1+'*3.14/180))*cos(("latitude"*3.14/180))*cos((('+lon1+' - "longitude")*3.14/180))))*180/3.14)*60*1.1515*1.609344) as distance from earthq) where distance <= '+distance+''
    # query1 = "SELECT * FROM (SELECT *,((acos(sin('"+ float(lat1) +"')*sin(LATITUDE) + cos('"+ float(lat1) +"')*cos(LATITUDE)*cos('"+ float(lon1) +"'-LONGITUDE))*6371) AS distance)) WHERE distance <= '"+ float(distance)"'"
    # query1 = "SELECT * FROM (select *,(((acos(sin(('"+lat1+"'*0.017444)) * sin((latitude*0.017444))+cos(('+"lat1+"'*0.017444))*cos((latitude*0.017444))*cos((('"+lon1+"' - longitude)*0.017444))))*57.3248)*60*1.1515*1.609344) as distance from earthq) where distance <= '+distance+'"
    # stmt2 = ibm_db.exec_immediate(conn, query2)
    # result2 = ibm_db.fetch_both(stmt2)
    # while result2:
    #     locationdist_data.append(result2)
    #     result2 = ibm_db.fetch_both(stmt2)

    return render_template('locationdist.html', table=locationdist_data, rowcount=len(locationdist_data), title='Location Distance')

def haversine(lon1, lat1, lon2, lat2):
    # """
    # Calculate the great circle distance between two points 
    # on the earth (specified in decimal degrees)
    # """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


@app.route("/morequakes", methods=["POST", "GET"])
def morequakes():
    latdeg1 = request.form.get("lat1")
    londeg1 = request.form.get("lon1")
    latdeg2 = request.form.get("lat2")
    londeg2 = request.form.get("lon2")
    magnitude = request.form.get("magnitude")
    
    quake_data = []
    # diff_min = lon1 * 4
    # local = float(gmttime) + float(diff_min)

    lat1 = math.radians(latdeg1)
    lon1 = math.radians(londeg1)
    lat2 = math.radians(latdeg2)
    lon2 = math.radians(londeg2)

    latlon = haversine(lon1, lat1, lon2, lat2)
    query1 = "SELECT * FROM EARTHQ WHERE MAG = '" + str(magnitude) + "' AND LATITUDE = '" + str(lat1) + "' AND LONGITUDE = '" + str(lon1) + "'"

    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        quake_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('morequakes.html', table=quake_data, rowcount=len(quake_data), title='More Earthquakes')




port = os.getenv('PORT', '5000')

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=int(port))
    app.run(host='0.0.0.0', port=int(port))
