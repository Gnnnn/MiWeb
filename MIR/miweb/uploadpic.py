import time
import os
import math
import re


def handle_uploaded_file(f):
    file_name = ""
    try:
        path = "static/miweb/images/upload" + time.strftime('/%Y/%m/%d/')
        loadway = "upload" +  time.strftime('/%Y/%m/%d/')
        path = "static/miweb/images/" + loadway
        if not os.path.exists(path):
            os.makedirs(path)
        f.name
        re.findall(r'\.(.*?)', f.name)
        name = str(int(math.floor(time.time() * 1000))) + "pic.jpeg"
        file_name = path + name
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        file_name = loadway + name
    except Exception, e:
        print e
    namelist = [file_name, name]
    return namelist


def handle_delete_file(file_path):
    pass