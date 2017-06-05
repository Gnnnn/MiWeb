import cv2
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import mysql.connector
import math
import shutil

def com(img):
    shutil.rmtree('static/miweb/images/temp_img/')
    path = 'static/miweb/images/temp_img/' + img.name
    default_storage.save(path, ContentFile(img.read()))
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    sift = cv2.SIFT()
    kp1 = sift.detect(img, None)
    points = []
    for i in kp1[:8]:
        point = str(round(i.pt[0], 2)) + ":" + str(round(i.pt[1], 2))
        #point = point.decode('utf-8')
        points.append(point)
    for i in range(len(points), 8):
        points.append("0:0")
    #print(points)
    #os.remove(path)
    conn = mysql.connector.connect(user='root', password='1234567a', database='miweb')
    cursor = conn.cursor()
    cursor.execute('select * from miweb_img_feature_point')
    values = cursor.fetchall()
    compare_result = []
    for value in values:
        dis = 0
        for i in range(3, 11):
            record_point = value[i].split(":")
            now_point = points[i-3].split(":")
            distance = math.sqrt(pow(float(record_point[0]) - float(now_point[0]), 2)) + math.sqrt(pow(float(record_point[1]) - float(now_point[1]), 2))
            dis += distance**2
        dis = math.sqrt(dis)
        compare_result.append([dis, value[1]])
    #print(compare_result)
    compare_result.sort()
    #print(compare_result)
    return path, compare_result[:30]