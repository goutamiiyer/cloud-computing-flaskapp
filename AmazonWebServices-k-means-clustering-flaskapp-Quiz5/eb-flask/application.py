from flask import Flask, request, render_template
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv,base64,time
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


# @application.route("/show", methods=["POST", "GET"])
# def show():
#     range1 = float(request.form.get('range1', ''))
#     range2 = float(request.form.get('range2', ''))
#     range3 = float(request.form.get('range3', ''))
#     range4 = float(request.form.get('range4', ''))
#
#     data = []
#
#     sql1 = "SELECT count(age) FROM dbo.titanic WHERE AGE BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
#     cursor.execute(sql1)
#     rows1 = cursor.fetchall()
#     sql2 = "SELECT count(fare) FROM dbo.titanic WHERE fare BETWEEN '" + str(range3) + "' AND '" + str(range4) + "'"
#     cursor.execute(sql2)
#     rows2 = cursor.fetchall()
#     data = pd.DataFrame(list(zip(rows1, rows2)), columns=['age', 'fare'])
#
#     return render_template('show.html', data=data)


def readbytesfile(file_name):
    data=open(file_name,'rb').read()
    return data


# https://stackoverflow.com/questions/40828929/sklearn-mean-distance-from-centroid-of-each-cluster
# Calculate Euclidean distance for each data point assigned to centroid
def k_mean_distance(data, cx, cy, i_centroid, cluster_labels):
    distances = [np.sqrt((x - cx) ** 2 + (y - cy) ** 2) for (x, y) in data[cluster_labels == i_centroid]]
    # return the mean value
    return np.mean(distances)


@application.route("/ycluster", methods=["POST", "GET"])
def ycluster():
    ylist = []
    file_name = "static/minnow.csv"
    cluster_num = int(request.form['cluster'])
    attribute1 = request.form['attribute1']
    attribute2 = request.form['attribute2']
    val1 = []
    val2 = []
    if attribute1 == "cabin":
        a = 0
    if attribute1 == "fname":
        a = 1
    if attribute1 == "lname":
        a = 2
    if attribute1 == "age":
        a = 3
    if attribute1 == "height":
        a = 4
    if attribute1 == "education":
        a = 5
    if attribute1 == "wealth":
        a = 6
    if attribute1 == "survived":
        a = 7
    if attribute1 == "lat":
        a = 8
    if attribute1 == "long":
        a = 9
    if attribute1 == "fare":
        a = 10
    if attribute2 == "cabin":
        b = 0
    if attribute2 == "fname":
        b = 1
    if attribute2 == "lname":
        b = 2
    if attribute2 == "age":
        b = 3
    if attribute2 == "height":
        b = 4
    if attribute2 == "education":
        b = 5
    if attribute2 == "wealth":
        b = 6
    if attribute2 == "survived":
        b = 7
    if attribute2 == "lat":
        b = 8
    if attribute2 == "long":
        b = 9
    if attribute2 == "fare":
        b = 10

    start_time = time.time()
    f = open(file_name)
    for row in csv.reader(f):
        try:
            valx = row[a]
            if a == 0 or a == 3 or a == 4 or a == 5 or a == 6 or a == 8 or a == 9 or a == 10:
                valx = int(valx)

            valy = row[b]
            if b == 0 or b == 3 or b == 4 or b == 5 or b == 6 or b == 8 or b == 9 or b == 10:
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

    end_time = time.time()
    elapsed_time = end_time-start_time
    fields = zip(c_mean_distances, length, centroids)

    p=[]
    for i in range(km.n_clusters):
        p.append(final[np.where(labels == i)])

    return render_template("ycluster.html", length=length, points=str(points), distance=c_mean_distances, fields=fields,
                           centroids=centroids, p=p, dists=dists, elapsed_time=elapsed_time)


@application.route("/cluster", methods=["POST", "GET"])
def cluster():
    ylist = []
    file_name = "static/minnow.csv"
    cluster_num = int(request.form['cluster'])
    attribute1 = request.form['attribute1']
    attribute2 = request.form['attribute2']
    range1 = (request.form.get('range1', ''))
    range2 = (request.form.get('range2', ''))
    range3 = (request.form.get('range3', ''))
    range4 = (request.form.get('range4', ''))
    val1 = []
    val2 = []
    if attribute1 == "cabin":
        a = 0
    if attribute1 == "fname":
        a = 1
    if attribute1 == "lname":
        a = 2
    if attribute1 == "age":
        a = 3
    if attribute1 == "height":
        a = 4
    if attribute1 == "education":
        a = 5
    if attribute1 == "wealth":
        a = 6
    if attribute1 == "survived":
        a = 7
    if attribute1 == "lat":
        a = 8
    if attribute1 == "long":
        a = 9
    if attribute1 == "fare":
        a = 10
    if attribute2 == "cabin":
        b = 0
    if attribute2 == "fname":
        b = 1
    if attribute2 == "lname":
        b = 2
    if attribute2 == "age":
        b = 3
    if attribute2 == "height":
        b = 4
    if attribute2 == "education":
        b = 5
    if attribute2 == "wealth":
        b = 6
    if attribute2 == "survived":
        b = 7
    if attribute2 == "lat":
        b = 8
    if attribute2 == "long":
        b = 9
    if attribute2 == "fare":
        b = 10

    start_time = time.time()
    f = open(file_name)
    for row in csv.reader(f):
        try:
            valx = row[a]
            if a == 0 or a == 3 or a == 4 or a == 5 or a == 6 or a == 8 or a == 9 or a == 10:
                valx = int(valx)
                range1 = int(range1)
                range2 = int(range2)

            valy = row[b]
            if b == 0 or b == 3 or b == 4 or b == 5 or b == 6 or b == 8 or b == 9 or b == 10:
                valy = int(valy)
                range3 = int(range3)
                range4 = int(range4)

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

    max_dist = []
    for i in range(1, cluster_num+1):
        tri_dists = dists[np.triu_indices(i)]
        maxdist=tri_dists.max()
        max_dist.append(maxdist)

# Calculate the mean distance
# distance between each data point of a cluster to their respective cluster centroids
    c_mean_distances = []
    for i, (cx, cy) in enumerate(centroids):
        # Calculate Euclidean distance for each data point assigned to centroid
        mean_distance = k_mean_distance(final, cx, cy, i, labels)
        c_mean_distances.append(mean_distance)

    length = {len(final[np.where(labels == i)]) for i in range(km.n_clusters)}
    points = {i: final[np.where(labels == i)] for i in range(km.n_clusters)}

    end_time = time.time()
    elapsed_time = end_time-start_time
    fields = zip(c_mean_distances, length, centroids)

    p=[]
    for i in range(km.n_clusters):
        p.append(final[np.where(labels == i)])

    return render_template("cluster.html", length=length, points=str(points), distance=c_mean_distances, fields=fields,
                           centroids=centroids, p=p, dists=dists, elapsed_time=elapsed_time, max_dist=max_dist)


@application.route("/piecluster", methods=["POST", "GET"])
def piecluster():
    ylist = []
    file_name = "static/minnow.csv"
    cluster_num = int(request.form['cluster'])
    attribute1 = request.form['attribute1']
    attribute2 = request.form['attribute2']
    range1 = (request.form.get('range1', ''))
    range2 = (request.form.get('range2', ''))
    range3 = (request.form.get('range3', ''))
    range4 = (request.form.get('range4', ''))
    val1 = []
    val2 = []
    if attribute1 == "cabin":
        a = 0
    if attribute1 == "fname":
        a = 1
    if attribute1 == "lname":
        a = 2
    if attribute1 == "age":
        a = 3
    if attribute1 == "height":
        a = 4
    if attribute1 == "education":
        a = 5
    if attribute1 == "wealth":
        a = 6
    if attribute1 == "survived":
        a = 7
    if attribute1 == "lat":
        a = 8
    if attribute1 == "long":
        a = 9
    if attribute1 == "fare":
        a = 10
    if attribute2 == "cabin":
        b = 0
    if attribute2 == "fname":
        b = 1
    if attribute2 == "lname":
        b = 2
    if attribute2 == "age":
        b = 3
    if attribute2 == "height":
        b = 4
    if attribute2 == "education":
        b = 5
    if attribute2 == "wealth":
        b = 6
    if attribute2 == "survived":
        b = 7
    if attribute2 == "lat":
        b = 8
    if attribute2 == "long":
        b = 9
    if attribute2 == "fare":
        b = 10

    start_time = time.time()
    f = open(file_name)
    for row in csv.reader(f):
        try:
            valx = row[a]
            if a == 0 or a == 3 or a == 4 or a == 5 or a == 6 or a == 8 or a == 9 or a == 10:
                valx = int(valx)
                range1 = int(range1)
                range2 = int(range2)

            valy = row[b]
            if b == 0 or b == 3 or b == 4 or b == 5 or b == 6 or b == 8 or b == 9 or b == 10:
                valy = int(valy)
                range3 = int(range3)
                range4 = int(range4)

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


    tri_dists = dists[np.triu_indices(cluster_num)]
    max_dist=tri_dists.max()

# Calculate the mean distance
# distance between each data point of a cluster to their respective cluster centroids
    c_mean_distances = []
    for i, (cx, cy) in enumerate(centroids):
        # Calculate Euclidean distance for each data point assigned to centroid
        mean_distance = k_mean_distance(final, cx, cy, i, labels)
        c_mean_distances.append(mean_distance)

    length = {len(final[np.where(labels == i)]) for i in range(km.n_clusters)}
    points = {i: final[np.where(labels == i)] for i in range(km.n_clusters)}

    end_time = time.time()
    elapsed_time = end_time-start_time
    fields = zip(c_mean_distances, length, centroids)

    p=[]
    for i in range(km.n_clusters):
        p.append(final[np.where(labels == i)])

    sql1 = "SELECT count('" + str(attribute1) + "') FROM dbo.minnow WHERE '" + str(attribute1) + "' BETWEEN '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(sql1)
    rows1 = cursor.fetchall()
    sql2 = "SELECT count('" + str(attribute2) + "') FROM dbo.minnow WHERE '" + str(attribute2) + "' BETWEEN '" + str(range3) + "' AND '" + str(range4) + "'"
    cursor.execute(sql2)
    rows2 = cursor.fetchall()

    rows = ([
        ['the centroid of a cluster', 'number of points in that cluster'],
        [str(range1) + '-' + str(range2), rows1[0][0]],
        [str(range3) + '-' + str(range4), rows2[0][0]]

    ])

    val = []
    for vals in row:
        val.append(int(vals))
    total = 0
    for vals in val:
        total = total + vals
    labels = ["the centroid of a cluster", "number of points in that cluster"]
    legendtab=[]
    for i in range(len(labels)):
        legendtab.append(labels[i] + " - " + str(round(val[i] / total * 100, 2)) + "%")

    patch = plt.pie(val, shadow=False, startangle=140, pctdistance=0.9, radius=2)
    plt.legend(patch[0], legendtab, bbox_to_anchor=(0.5, 0.5), bbox_transform=plt.gcf().transFigure, loc="best")
    plt.axis("equal")
    plt.title("the centroid of cluster")
    plt.tight_layout()
    plt.show()
    plt.savefig("visualization.png")
    plt.clf()
    fileinfo = base64.b64encode(readbytesfile("visualization.png")).decode()

    return render_template("piecluster.html", length=length, points=str(points), distance=c_mean_distances, fields=fields,
                           centroids=centroids, p=p, dists=dists, elapsed_time=elapsed_time, max_dist=max_dist, fileinfo="data:image/jpg;base64,"+fileinfo)


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