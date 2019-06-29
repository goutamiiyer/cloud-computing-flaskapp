from flask import Flask, request, render_template
import os
import pandas as pd
import csv,base64
import pymysql
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
from scipy.spatial import distance


application = Flask(__name__)

db = pymysql.connect(user='',
                     password='',
                     host='',
                     cursorclass=pymysql.cursors.DictCursor)
# Enter user, password and host. Deleted for security purposes
cursor = db.cursor()


@application.route("/")
def home():
    return render_template('home.html')


@application.route("/show", methods=["POST", "GET"])
def show():
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))

    data = []

    sql1 = "SELECT count(age) FROM dbo.titanic WHERE AGE BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(sql1)
    rows1 = cursor.fetchall()
    sql2 = "SELECT count(fare) FROM dbo.titanic WHERE fare BETWEEN '" + str(range3) + "' AND '" + str(range4) + "'"
    cursor.execute(sql2)
    rows2 = cursor.fetchall()
    data = pd.DataFrame(list(zip(rows1, rows2)), columns=['age', 'fare'])

    return render_template('show.html', data=data)


# https://stackoverflow.com/questions/40828929/sklearn-mean-distance-from-centroid-of-each-cluster
# Calculate Euclidean distance for each data point assigned to centroid
def k_mean_distance(data, cx, cy, i_centroid, cluster_labels):
    distances = [np.sqrt((x - cx) ** 2 + (y - cy) ** 2) for (x, y) in data[cluster_labels == i_centroid]]
    # return the mean value
    return np.mean(distances)


@application.route("/ycluster", methods=["POST", "GET"])
def ycluster():
    ylist = []
    file_name = "static/titanic3.csv"
    cluster_num = int(request.form['cluster'])
    attribute1 = request.form['attribute1']
    attribute2 = request.form['attribute2']
    val1 = []
    val2 = []
    if attribute1 == "pclass":
        a = 0
    if attribute1 == "survived":
        a = 1
    if attribute1 == "name":
        a = 2
    if attribute1 == "sex":
        a = 3
    if attribute1 == "age":
        a = 4
    if attribute1 == "sibsp":
        a = 5
    if attribute1 == "ticket":
        a = 6
    if attribute1 == "fare":
        a = 7
    if attribute1 == "cabin":
        a = 8
    if attribute1 == "embarked":
        a = 9
    if attribute1 == "boat":
        a = 10
    if attribute1 == "body":
        a = 11
    if attribute1 == "dest":
        a = 12
    if attribute2 == "pclass":
        b = 0
    if attribute2 == "survived":
        b = 1
    if attribute2 == "name":
        b = 2
    if attribute2 == "sex":
        b = 3
    if attribute2 == "age":
        b = 4
    if attribute2 == "sibsp":
        b = 5
    if attribute2 == "ticket":
        b = 6
    if attribute2 == "fare":
        b = 7
    if attribute2 == "cabin":
        b = 8
    if attribute2 == "embarked":
        b = 9
    if attribute2 == "boat":
        b = 10
    if attribute2 == "body":
        b = 11
    if attribute2 == "dest":
        b = 12

    f = open(file_name)
    for row in csv.reader(f):
        try:
            valx = row[a]
            if a == 4 or a == 7:
                valx = float(row[a])
            if a == 0 or a == 1 or a == 5 or a == 11:
                valx = int(valx)

            valy = row[b]
            if b == 4 or b == 7:
                valy = float(row[b])
            if b == 0 or b == 1 or b == 5 or b == 11:
                valy = int(valy)

            if valy not in ylist:
                ylist.append(valy)
            listyindex = ylist.index(valy)
            val1.append(valx)
            val2.append(listyindex)
        except ValueError:
            continue

    datal = []
    udatal = []
    for i in range(0, len(val1) - 1):
        datal.append(val1[i])
        datal.append(val2[i])
        udatal.append(datal)
        datal = []

    final = np.array(udatal)

    km = KMeans(n_clusters=cluster_num).fit(final)
    labels = km.labels_
    centroids = km.cluster_centers_
    dists = euclidean_distances(km.cluster_centers_)

# Calculate the mean distance
# distance between each data point of a cluster to their respective cluster centroids
    c_mean_distances = []
    for i, (cx, cy) in enumerate(centroids):
        # Calculate Euclidean distance for each data point assigned to centroid
        mean_distance = k_mean_distance(final, cx, cy, i, labels)
        c_mean_distances.append(mean_distance)

    length = {len(final[np.where(labels == i)]) for i in range(km.n_clusters)}
    points = {i: final[np.where(labels == i)] for i in range(km.n_clusters)}

    fields = zip(c_mean_distances, length, centroids)

    p=[]
    for i in range(km.n_clusters):
        p.append(final[np.where(labels == i)])

    return render_template("ycluster.html", length=length, points=str(points), distance=c_mean_distances, fields=fields,
                           centroids=centroids, p=p, dists=dists)


@application.route("/xycluster", methods=["POST", "GET"])
def xycluster():
    ylist = []
    xlist = []
    file_name = "static/titanic3.csv"
    cluster_num = int(request.form['cluster'])
    attribute1 = request.form['attribute1']
    attribute2 = request.form['attribute2']
    val1 = []
    val2 = []
    if attribute1 == "pclass":
        a = 0
    if attribute1 == "survived":
        a = 1
    if attribute1 == "name":
        a = 2
    if attribute1 == "sex":
        a = 3
    if attribute1 == "age":
        a = 4
    if attribute1 == "sibsp":
        a = 5
    if attribute1 == "ticket":
        a = 6
    if attribute1 == "fare":
        a = 7
    if attribute1 == "cabin":
        a = 8
    if attribute1 == "embarked":
        a = 9
    if attribute1 == "boat":
        a = 10
    if attribute1 == "body":
        a = 11
    if attribute1 == "dest":
        a = 12
    if attribute2 == "pclass":
        b = 0
    if attribute2 == "survived":
        b = 1
    if attribute2 == "name":
        b = 2
    if attribute2 == "sex":
        b = 3
    if attribute2 == "age":
        b = 4
    if attribute2 == "sibsp":
        b = 5
    if attribute2 == "ticket":
        b = 6
    if attribute2 == "fare":
        b = 7
    if attribute2 == "cabin":
        b = 8
    if attribute2 == "embarked":
        b = 9
    if attribute2 == "boat":
        b = 10
    if attribute2 == "body":
        b = 11
    if attribute2 == "dest":
        b = 12

    f = open(file_name)
    for row in csv.reader(f):
        try:
            valx = row[a]
            if a == 4 or a == 7:
                valx = float(row[a])
            if a == 0 or a == 1 or a == 5 or a == 11:
                valx = int(valx)

            if valx not in xlist:
                xlist.append(valx)
            listxindex = xlist.index(valx)

            valy = row[b]
            if b == 4 or b == 7:
                valy = float(row[b])
            if b == 0 or b == 1 or b == 5 or b == 11:
                valy = int(valy)

            if valy not in ylist:
                ylist.append(valy)
            listyindex = ylist.index(valy)
            val1.append(listxindex)
            val2.append(listyindex)
        except ValueError:
            continue

    datal = []
    udatal = []
    for i in range(0, len(val1) - 1):
        datal.append(val1[i])
        datal.append(val2[i])
        udatal.append(datal)
        datal = []

    final = np.array(udatal)

    km = KMeans(n_clusters=cluster_num).fit(final)
    labels = km.labels_
    centroids = km.cluster_centers_

    # Calculate the mean distance
    c_mean_distances = []
    for i, (cx, cy) in enumerate(centroids):
        # Calculate Euclidean distance for each data point assigned to centroid
        mean_distance = k_mean_distance(final, cx, cy, i, labels)
        c_mean_distances.append(mean_distance)

    length = {len(final[np.where(labels == i)]) for i in range(km.n_clusters)}
    points = {i: final[np.where(labels == i)] for i in range(km.n_clusters)}

    fields = zip(c_mean_distances, length, centroids)

    p = []
    for i in range(km.n_clusters):
        p.append(final[np.where(labels == i)])

    return render_template("xycluster.html", length=length, points=str(points), distance=c_mean_distances, fields=fields,
                           centroids=centroids, p=p)


@application.route("/dbcluster", methods=["POST", "GET"])
def dbcluster():
    cluster_num = int(request.form['cluster'])
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    val1 = []
    val2 = []

    sql1 = "SELECT count(age) FROM dbo.titanic where AGE BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(sql1)
    rows1 = cursor.fetchall()
    for vals in rows1[0]:
        val1.append(float(vals))
    sql2 = "SELECT count(fare) FROM dbo.titanic where fare BETWEEN '" + str(range3) + "' AND '" + str(range4) + "'"
    cursor.execute(sql2)
    rows2 = cursor.fetchall()
    for vals in rows2[0]:
        val2.append(float(vals))

    datal = []
    udatal = []
    for i in range(0, len(val1) - 1):
        datal.append(val1[i])
        datal.append(val2[i])
        udatal.append(datal)
        datal = []

    final = np.array(udatal)

    km = KMeans(n_clusters=cluster_num).fit(final)
    labels = km.labels_
    centroids = km.cluster_centers_

# Calculate the mean distance
    c_mean_distances = []
    for i, (cx, cy) in enumerate(centroids):
        # Calculate Euclidean distance for each data point assigned to centroid
        mean_distance = k_mean_distance(final, cx, cy, i, labels)
        c_mean_distances.append(mean_distance)

    length = {len(final[np.where(labels == i)]) for i in range(km.n_clusters)}
    points = {i: final[np.where(labels == i)] for i in range(km.n_clusters)}

    fields = zip(c_mean_distances, length, centroids)

    p=[]
    for i in range(km.n_clusters):
        p.append(final[np.where(labels == i)])

    return render_template("dbcluster.html", length=length, points=str(points), distance=c_mean_distances, fields=fields,
                           centroids=centroids, p=p)


if __name__ == "__main__":
    application.debug = True
    application.run()