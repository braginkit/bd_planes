from glob import glob

import json
from flask import jsonify

from pymongo import MongoClient
import datetime

hostDB = 'localhost'
portDB = 27017

#prompt the user for a file to import

#filename = rs.OpenFileName("Open JSON File", "./json/" + filter)

def connection_to_db():
    client = MongoClient(hostDB, portDB)
    db = client['flights_today']
    return db['flights']

def open_json(flag):
    connect = connection_to_db()

    data = []
    check = 0
    for t in connect.find({}, {"_id": 0}):
        if (check > 20) and flag:
            check = 0
            break
        data.append(t)

        line = []

        line2 = []

        for i in t["Way"]["coordinates"]["points"]:
            l = []
            l.append(float(i["longitude"]))
            l.append(float(i["latitude"]))

            #1.append (round (float (t ["Way"] ["flights”] ["rounds”] [0] ["emissionsforpointless"]),2)):
            line.append(l)

            #line2.append(1[0:2]);
        del t["Way"]["coordinates"]["points"]
        t["Way"]["coordinates"]["points"] = line
        #t["Way"] ["coordinates”] ["points"] = line2

        check += 1

    return data
# выборка инфы по дате
def get_by_date(date_in):
    date_t = []
    date_t.append(datetime.datetime.strptime(date_in[0], '%Y-%m-%d').date())
    date_t.append(datetime.datetime.strptime(date_in[1], '%Y-%m-%d').date())
    new_arr = []
    data = open_json(0)
    #k=0
    for i in data:
        date_arr = []
        for j in range(0, len(i["Way"]["flights"]["rounds"])):
            tmp_date = datetime.datetime.strptime(i["Way"]["flights"]["rounds"][j]["data"], '%d.%m.%Y').date()
            #print (tmp_date)
            if (date_t[0] <= tmp_date <= date_t[1]):
                date_arr.append(i["Way"]["flights"]["rounds"][j])
        i["Way"]["flights"]["rounds"].clear()
        if (len(date_arr) != 0):
            i["Way"]["flights"]["rounds"] = date_arr
            new_arr.append(i)
    return new_arr

    #print (new_arr[0] ["Way"] ["flights”] ["rounds”])
#Подсчет статистики, выбросов на линию вывод всей информации на линию и вообще

def stat(data):
    new_arr = data
    co2_min_all = 0
    co2_max_all = 0
    air_count_all = 0
    km_all = 0
    air_list_all = []

    print("Stat")

    for i in new_arr:
        if (len(i["Way"]["flights"]["rounds"]) == 1):
            pass
        else:

            co2_max = 0
            co2_min = 0

            d = dict.fromkeys(list(dict.keys(new_arr[0]["Way"]["flights"]["rounds"][0])), None)
            d["totalfuelwastedless"] = 0
            d["totalfuelwastedmax"] = 0
            d["coefficientoftheseatsless"] = []
            d["coefficientoftheseatsmax"] = []
            d["airplane"] = []
            air_count_all += len(i["Way"]["flights"]["rounds"])

            print("Stat 2")

            d["data"] = i["Way"]["flights"]["rounds"][0]["data"] + "-" + i["Way"]["flights"]["rounds"][-1]["data"]
            for j in i["Way"]["flights"]["rounds"]:
                co2_min_all += len(i["Way"]["coordinates"]["points"]) * j["emissionsforpointless"]
                co2_max_all += len(i["Way"]["coordinates"]["points"]) * j["emissionsforpointmax"]
                co2_min += len(i["Way"]["coordinates"]["points"]) * j["emissionsforpointless"]
                co2_max += len(i["Way"]["coordinates"]["points"]) * j["emissionsforpointmax"]
                km_all += j["km"]
                d["totalfuelwastedless"] += j["totalfuelwastedless"]
                d["totalfuelwastedmax"] += j["totalfuelwastedmax"]


                d["km"] = j["km"]
                if not (j["airplane"] in d["airplane"]):
                    d["airplane"].append(j["airplane"])

                    d["coefficientoftheseatsless"].append(j["coefficientoftheseatsless"])

                    d["coefficientoftheseatsmax"].append(j["coefficientoftheseatsmax"])

            air_list_all.extend(d["airplane"])

            d["totalemissionsless"] = co2_min

            d["totalemissionsmax"] = co2_max

            d["airplane"] = ", ".join(d["airplane"])

            d["coefficientoftheseatsless"] =", ".join(d["coefficientoftheseatsless"])

            d["coefficientoftheseatsmax"] = ", ".join(d["coefficientoftheseatsmax"])

            #print (type (i["Way"] ["flights”] ["rounds”]))

            i["Way"]["flights"]["rounds"].clear()

            i["Way"]["flights"]["rounds"].append(d)
    print("Stat 3")

    print()
    all_Ways = {
        "co2_min_all": co2_min_all,
        "co2_max_all": co2_max_all,
        #"km_all" : km_all,
        "air_list_all": list(set(air_list_all)),
        "air_count_all": air_count_all
    }
    print(all_Ways)
    return [all_Ways, new_arr]

def filter_air_local(data, air_list):
    res_i = []
    res = []
    if (len(air_list) < 2):
        return jsonify([])
    for i in range(0, len(air_list), 2):
        for j in range(0, len(data)):
            if (data[j]['Way']['from'] == air_list[i] and data[j]['Way']['to'] == air_list[i+1]):
                res_i.append(j)

    for i in res_i:
        res.append(data[i])

    return res

def filter_area_local(data, xy):
    xy = [
        [min(xy[0][0], xy[1][0]), min(xy[0][1], xy[1][1])],
        [max(xy[0][0], xy[1][0]), max(xy[0][1], xy[1][1])]
    ]
    allPointsNew = []
    new_data = []
    for i in range(0, len(data)):
        allPointst = []
        for j in range(0, len(data[i]["Way"]["coordinates"]["points"])):
            if (((data[i]["Way"]["coordinates"]["points"][j][0] >= xy[0][0]) and (data[i]["Way"]["coordinates"]["points"][j][0] <= xy[1][0])) and ((data[i]["Way"]["coordinates"]["points"][j][1] >= xy[0][1]) and (data[i]["Way"]["coordinates"]["points"][j][1] <= xy[1][1]))):
                allPointst.append(data[i]["Way"]["coordinates"]["points"][j])
        if (len(allPointst) != 0):

            #print (allPointst)
            #print ("del "+ str(i))

#========================================
            # del data[i] ["Way"] ["coordinates”] ["points1"]

            new_data.append(data[i])

            new_data[-1]["Way"]["coordinates"]["points"] = allPointst

            # print (allPointst)

            # print (i["Way"] ["coordinates"])

    return new_data

def filt_area(xy, flag):
    connect = connection_to_db()
    data = []
    check = 0
    xy = [
        [min(xy[0][0], xy[1][0]), min(xy[0][1], xy[1][1])],

        [max(xy[0][0], xy[1][0]), max(xy[0][1], xy[1][1])]
    ]

    for t in connect.find({"$and": [{"Way.coordinates.points.longitude": {"$gt": str(xy[0][0]), "$lt": str(xy[1][0])}},
                                    {"Way.coordinates.points.latitude": {"$gt": str(xy[0][1]), "$lt":str(xy[1][1])}}]}, {"_id": 0}):

        if (check > 20) and flag:
            check = 0
            break

        line = []

        line2 = []

        for i in t["Way"]["coordinates"]["points"]:
            l = []
            l.append(float(i["longitude"]))
            l.append(float(i["latitude"]))

            line.append(l)
            #line2.append(1[0:2])

        del t["Way"]["coordinates"]["points"]
        t["Way"]["coordinates"]["points"] = line
        #t["Way"] ["coordinates"] ["points"] = line2;
        data.append(t)
        check += 1
    allPointsNew = []
    new_data = []
    for i in range(0,len(data)):
        allPointst = []
        for j in range(0, len(data[i]["Way"]["coordinates"]["points"])):
            if (((data[i]["Way"]["coordinates"]["points"][j][0] >= xy[0][0]) and (data[i]["Way"]["coordinates"]["points"][j][0] <= xy[1][0])) and ((data[i]["Way"]["coordinates"]["points"][j][1] >= xy[0][1]) and (data[i]["Way"]["coordinates"]["points"][j][1] <= xy[1][1]))):
                allPointst.append(data[i]["Way"]["coordinates"]["points"][j])

        if (len(allPointst) != 0):

            #print (allPointst)

            #print ("del "+ str(i))

            #del data[i] ["Way"] ["coordinates"] ["points1"]

            new_data.append(data[i])

            new_data[-1]["Way"]["coordinates"]["points"] = allPointst

            #print (allPointst)

            #print (i["Way"] ["coordinates"])

    return new_data

#return only points from ways
def open_json_points(flag):

    connect = connection_to_db()
    allPoints = []

    check = 0

    for x in connect.find({}, {"_id": 0}):
        if (check > 20) and flag:
            check = 0
            break

        points = []

        for i in x["Way"]['coordinates']['points']:
            #print (i['longitude'],i['latitude'])
            t = []
            t.append(float(i['longitude']))
            t.append(float(i['latitude']))

            #t.append (float (x["Way"] ["flights”] ["rounds”] [0] ["emissionsforpointless"1))

            points.append(t)
        allPoints.append(points)

    return allPoints

#return list of airoport
def list_airoports():
    data = open_json(0)
    airoports = []
    for i in data:
        if (i['Way']['from'] not in airoports):
            airoports.append(i['Way']['from'])
        if (i['Way']['to'] not in airoports):
            airoports.append(i['Way']['to'])

    return airoports
