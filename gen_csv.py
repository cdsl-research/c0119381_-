
import sys, io
from tabnanny import check
from pymongo import *
from datetime import date
import csv

def deleteCollection():
    client = MongoClient("mongodb://sirius:sgt945518@localhost:27017/")
    collection = client["yamamoto"]["distance_total"] #client[データベース名][コレクション名]
    collection.drop()

def mongod():
    client = MongoClient("mongodb://sirius:sgt945518@localhost:27017/")
    db = client.yamamoto
    collection = db.distance_total
    find =  collection.find(projection={'_id':0})
    return find

def getData():
    find = mongod()
    count = 0
    timeList = list()
    disV1 = list()
    disV2 = list()
    disV3 = list()
    nameList  = list()
    for doc in find:
        if doc["time"] != None:
            time = doc['time']
            distanceV1 = doc["distance1"]
            distanceV2 = doc["distance2"]
            distanceV3 = doc["distance3"]
            timeList.append(time)
            disV1.append(distanceV1)
            disV2.append(distanceV2)
            disV3.append(distanceV3)    
    
    
    return timeList,disV1,disV2,disV3

def main():
    timeList,disV1,disV2,disV3 = getData()
    # distanceListに距離データが格納されている
    # distanceListは２重配列
    timeL = list()
    disL1 = list()
    disL2 = list()
    disL3 = list()
    countTotal = 0
    csvWriteList = list()
    for i in range(len(timeList)):
        # timeList[i] = list(reversed(timeList[i]))
        # disV1[i] = list(reversed(disV1[i]))
        # disV2[i] = list(reversed(disV2[i]))
        # disV3[i] = list(reversed(disV3[i]))
        for j in range(len(timeList[i])): # range()の中を任意の数字で置き換えることで直近のデータ数を指定可能            
            disL1.append(disV1[i][j])
            disL2.append(disV2[i][j])
            disL3.append(disV3[i][j])
    # disL1 = list(reversed(disL1))
    # disL2 = list(reversed(disL2))
    # disL3 = list(reversed(disL3))
    for i in range(len(disL1)):
        csvWriteChildList = list()
        d1 = disL1[i]
        d2 = disL2[i]
        d3 = disL3[i]
        csvWriteChildList.append(disL1[i])
        csvWriteChildList.append(disL2[i])
        csvWriteChildList.append(disL3[i])
        csvWriteList.append(csvWriteChildList)
                
    with open('/var/www/html/yamamoto/distance.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(csvWriteList)
if __name__ == "__main__":
    main()
    Q = input("データベースを削除するか？(y / n)")
    if Q == "y":
        deleteCollection()