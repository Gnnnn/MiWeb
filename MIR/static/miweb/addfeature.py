import mysql.connector
import cv2


conn = mysql.connector.connect(user='root', password='1234567a', database='miweb')
cursor = conn.cursor()
cursor.execute('select * from miweb_img')
values = cursor.fetchall()
for value in values[110:]:
    #print(value[16])
    path = 'images/' + value[8]
    path = path.replace('\\', '/')
    print(path)
    try:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        sift = cv2.SIFT()
        kp1 = sift.detect(img, None)
        points = []
        for i in kp1[:8]:
            point = str(round(i.pt[0], 2)) + ":" + str(round(i.pt[1], 2))
            #point = point.decode('utf-8')
            points.append(point)

        cursor.execute('insert into miweb_img_feature_point (id, img_id, img_type, img_feature1, img_feature2, img_feature3, img_feature4, img_feature5, img_feature6, img_feature7, img_feature8) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [value[0], value[16], 1, points[0], points[1], points[2], points[3], points[4], points[5], points[6], points[7]])
        conn.commit()
        print(points)
    except:
        pass
cursor.close()