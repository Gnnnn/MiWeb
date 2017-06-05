import time
import random


def genenum():
    word = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    timenum = str(int(time.time() * 1000))
    outputlist = ""
    for i in timenum:
        alnum = random.randint(0, 25)
        outputlist += str(word[alnum])
        outputlist += i
    return outputlist


def geneusernum():
    word = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    timenum = str(int(time.time() * 1000))
    outputlist = ""
    for i in range(0, 3):
        alnum = random.randint(0, 25)
        outputlist += str(word[alnum])
    outputlist += timenum
    for i in range(0, 5):
        alnum = random.randint(0, 25)
        outputlist += str(word[alnum])
    return outputlist