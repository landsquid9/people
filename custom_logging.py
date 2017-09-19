import logging
import time

def timeStamp():
    return str(time.asctime(time.localtime(time.time())))

def add(s):
    logging.info(timeStamp() + ": " + s)

def setup():
    resetLogFile()
    logging.basicConfig(filename='log.log',level=logging.DEBUG)
    add("log started")

def resetLogFile():
    f = open('log.log', 'w')
    f.close()
