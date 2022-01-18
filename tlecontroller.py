import urllib3
from datetime import datetime
import socket
import logging
import issglobeconfig as cfg

def updateIssTleData():
  # check internet connection
  # update file if connection
  # if no connection use data already in file
  logging.debug("Attempting to update ISS TLE data")
  if is_connected():
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://www.celestrak.com/NORAD/elements/stations.txt')
    tle = r.data.decode('utf-8').split("\n")[0:3]
    f = open("isstle.txt", "w")
    f.write(tle[0] + "\n" + tle[1] + "\n" + tle[2] + "\n" + "updated: " + str(datetime.now()))

  f = open(cfg.isstledir, "r")
  tle = f.read().split("\n")[0:3]
  return tle

def is_connected():
  try:
    # connect to the host -- tells us if the host is actually reachable
    socket.create_connection(("www.celestrak.com", 80))
    logging.debug("Connection to www.celestrak.com:80 succesfull. Will now get fresh ISS TLE... YUM")
    return True
  except Exception as e:
    logging.warning(e)
    logging.warning("Connection to  www.celestrak.com:80 was unsuccesfull. will use past TLE data")
    pass
  return False