import urllib3
from math import sin, cos, sqrt, atan2, radians
import math
#import time
from datetime import datetime
import ephem
from ephem import degree
import socket
#from threading import Timer
import select
import sys
from ledcontrol import scrollup, scrolldown, protectionShow, colorSetAll, rainbowColumnCycle
import logging
from neopixel import Color

degrees_per_radian = 180.0 / math.pi

sun = ephem.Sun()
moon = ephem.Moon()
greenwich = ephem.Observer()
greenwich.lat = "0"
greenwich.lon = "0"

sunLightRadius = ephem.earth_radius/1000 * 1.5 #earth radius should mean about 50% coverage
moonLightRadius = (ephem.earth_radius/1000)*.33 #1/3 earth radius
sunLightColor = Color(255,255,200) #yellow white
moonLightColor = Color(255,0,255) #light blue
issLightColor = Color(0,255,0) #red
totalNumLed = 40 #total number of leds on system
statusLed = 41 #number in chain of the status led
currMode = 0 #the current mode, starts at 0

# NEOPIXEL BEST PRACTICES for most reliable operation:
# // - Add 1000 uF CAPACITOR between NeoPixel strip's + and - connections.
# // - MINIMIZE WIRING LENGTH between microcontroller board and first pixel.
# // - NeoPixel strip's DATA-IN should pass through a 300-500 OHM RESISTOR.

def getLedCoords():
  f = open("/home/pi/issglobe/ledcoords.txt", "r")
  flines = f.read().split("\n")
  outputList = []
  for i in flines:
    outputList.append(eval(i))
  return outputList #0-399

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
  
  f = open("isstle.txt", "r")
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

def getPointWithinDist(lat, lon, distance, pointArray):
  lights = []
  for i in pointArray: #pointarray = 0-399
    x = i[0]
    y = i[1]
    dist = calcDist(lat, lon, x, y)
    if dist < distance:
      lights.append(pointArray.index(i))
  return lights

def getClosestPoint(lat, lon, pointArray):
  point = 0
  minDist = 100000
  for i in pointArray:
    # print(i)
    x = i[0]
    y = i[1]
    # print (lat, lon, x, y)
    dist = calcDist(lat, lon, x, y)
    # print (dist)
    # print("{},{},{}".format(x,y,round(dist,0)))
    if dist < minDist:
      point = pointArray.index(i)
#      coord = str(x)+","+str(y)
      minDist = dist
#       print (point, dist)
#       print (lat, lon, x, y)
  logging.debug("clostest point is: {}: ({}) with distance of: {}".format(point, pointArray[point], minDist))
#   print (lat,lon,pointArray[point][0], pointArray[point][1])
#   print (point, pointArray[point], minDist)
  
  return point

def getClosestPoints(lat, lon, pointArray, amount):
  tempPointArray = pointArray.copy()
  topDistList = []
  for y in range(amount):
    point = 0
    minDist = 100000
    for i in tempPointArray:
      x = i[0]
      y = i[1]
      dist = calcDist(lat, lon, x, y)
      # print(x,y,dist)
      if dist < minDist:
        point = tempPointArray.index(i)
        coord = str(x)+","+str(y)
        minDist = dist
        # print(pointArray.index(i), " : ", dist)
    closePointStr = str(coord) + " : " + str(minDist)
    topDistList.append(closePointStr)
    del tempPointArray[point]

  for i in topDistList:
    logging.debug("closest point ", topDistList.index(i), i)
  return topDistList

def calcDist(lat1, lon1, lat2, lon2):

  # approximate radius of earth in km
  R = (ephem.earth_radius/1000)
  lat1 = radians(lat1)
  lon1 = radians(lon1)
  lat2 = radians(lat2)
  lon2 = radians(lon2)
  dlon = (abs(lon2 - lon1))
  dlat = (abs(lat2 - lat1))
#   print (dlon, dlat)
  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))
  distance = R * c

  return distance

def lightSun(pointArray):
  sun.compute()
  sun_lon = math.degrees(sun.ra - greenwich.sidereal_time() )
  if sun_lon < -180.0 :
    sun_lon = 360.0 + sun_lon 
  elif sun_lon > 180.0 :
    sun_lon = sun_lon - 360.0
  sun_lat = math.degrees(sun.dec)
  # print ("Subsolar Point",sun_lon,sun_lat)
  lightsArray = getPointWithinDist(sun_lat, sun_lon, sunLightRadius,  pointArray)
  sunArray = []
  for i in lightsArray:
    sunArray.append((i, sunLightColor))
    # print("sun: ", pointArray[i])
  return sunArray

def lightMoon(pointArray):
  moon.compute()
  moonlon = moon.hlon / degree
  moonlat = moon.hlat /degree
  # print(moonLightRadius)
  lightsArray = getPointWithinDist(moonlat, moonlon, moonLightRadius,  pointArray)
  logging.debug("moon: {} {}".format(moonlat, moonlon))
  moonArray = []
  for i in lightsArray:
    moonArray.append((i, moonLightColor))
    # print("moon: ", pointArray[i])
  return moonArray

def lightIss(pointArray):
  tle = updateIssTleData()
  line1 = tle[0]
  line2 = tle[1]
  line3 = tle[2]
  iss = ephem.readtle(line1, line2, line3)
  iss.compute()
  isslong = iss.sublong / degree
  isslat = iss.sublat / degree
  logging.debug("Iss: %s %s" % (isslat, isslong))
  # getClosestPoints(isslat, isslong, pointArray, 3)
  lightsArray = [(getClosestPoint(isslat, isslong, pointArray),issLightColor)]
  # lightsArray = [(getClosestPoint(37, 160, pointArray),issLightColor)]
  return lightsArray

def runMode(currMode, strip):
  lightsArray = []
  led_coords = getLedCoords()
  if (int(currMode) == 0):
    # print("0iss")
    for i in lightIss(led_coords):
      lightsArray.append(i)
  elif (int(currMode) == 1):
    # print("1sun")
    for i in lightSun(led_coords):
      lightsArray.append(i)
  elif (int(currMode) == 2):
    # print("2moon")
    for i in lightMoon(led_coords):
      lightsArray.append(i)
  elif (int(currMode) == 3):
    # print("3all")
    for i in lightSun(led_coords):
      lightsArray.append(i)
    for i in lightMoon(led_coords):
      lightsArray.append(i)
    for i in lightIss(led_coords):
      lightsArray.append(i)
  elif (int(currMode) == 4):
      rainbowColumnCycle(strip, led_coords)

  colorSetAll(strip, Color(0,0,0))
  for i in lightsArray:
    strip.setPixelColor(i[0], i[1])
  protectionShow(strip)

def changeMode(currMode):
  #call this when button press
  modeList = [1,2,3,4,0]
  currMode = modeList[currMode]
  return currMode

def systemOn(strip):
  led_coords = getLedCoords()
  scrollup(strip, led_coords)

def systemOff(strip):
  led_coords = getLedCoords()
  scrolldown(strip, led_coords)

def getColumnArray(pointArray):
  #get array of points with each (point,column)
  columns = [0,11.25,22.5,33.75,45,56.25,67.5,78.75,90,101.25,112.5,123.75,135,146.25,157.5,168.75,180,191.25,202.5,213.75,225,236.25,247.5,258.75,270,281.25,292.5,303.75,315,326.25,337.5,348.75]
  columnArray = []
  for j in pointArray:
    columnArray.append((pointArray.index(j), columns.index(j[1])))
  return columnArray