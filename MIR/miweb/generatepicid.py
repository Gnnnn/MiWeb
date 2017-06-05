import time


def genepicid():
    now = time.time()
    t = "Jan 1 00:00:00 2016"
    p = time.mktime(time.strptime(t, "%b %d %H:%M:%S %Y"))
    s = now - p
    s *= 1000
    y = 'U'+'M'+'%d'%s+'00'
    return y