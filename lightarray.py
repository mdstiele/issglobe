import urllib3
# from math import sin, cos, sqrt, atan2, radians
import math
#import time
from datetime import datetime
import ephem
from ephem import degree
from geopy import distance as gdistance
import socket
#from threading import Timer
import select
import sys
from ledcontrol import scrollup, scrolldown, protectionShow, colorSetAll, rainbowColumnCycle
import logging
from neopixel_mock_ms import Color
from mapplot import plot

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
# currMode = 0 #the current mode, starts at 0
defaultMode = 0 #defualt mode when the system starts

ledCoordsDir = "ledcoords.txt"#"ledcoords.txt"#"/home/pi/issglobe/ledcoords.txt"

# NEOPIXEL BEST PRACTICES for most reliable operation:
# // - Add 1000 uF CAPACITOR between NeoPixel strip's + and - connections.
# // - MINIMIZE WIRING LENGTH between microcontroller board and first pixel.
# // - NeoPixel strip's DATA-IN should pass through a 300-500 OHM RESISTOR.

def readLedCoords():
  f = open(ledCoordsDir, "r")
  flines = f.read().split("\n")
  outputList = []
  for i in flines:
    outputList.append(eval(i))
  return outputList #0-399

def compute_row_col_list(pointarray):
  rowlist = []
  collist = []
  for i in pointarray:
    if i[1] not in rowlist:
      rowlist.append(i[1])
    if i[0] not in collist:
      collist.append(i[0])

  return rowlist, collist

# Lightarray class object will hold all variables related to the coordinates and also
#   the coord/led interaction
class Lightarray:
  def __init__(self):
    #sets led coord data to a tuple array
    self.ledcoords = readLedCoords()
    #num of pixels(leds)
    self.num_of_leds = len(self.ledcoords)
    #row list #col list
    self.led_row_list, self.led_col_list = compute_row_col_list(self.ledcoords)
    #row count
    self.num_of_led_row = len(self.led_row_list)
    #col count
    self.num_of_led_col = len(self.led_col_list)
    #read land data
    self.led_is_land = []
    #current mode
    self.mode = defaultMode
    self.lightsArray = []

  def getLedCoords(self):
    return self.ledcoords

  def setmode(self, mode: int):
    self.mode = mode

  def getmode(self):
    return self.mode

  def get_lights_array(self):
    return self.lightsArray

  def clearlightsarray(self):
    self.lightsArray = []

  # def compute_row_col_list(self):
  #   rowlist = []
  #   collist = []
  #   for i in self.getLedCoords():
  #     if i[0] not in rowlist:
  #       rowlist.append(i[1])
  #     if i[1] not in collist:
  #       collist.append(i[0])
  #   print(rowlist)
  #   self.led_row_list = rowlist
  #   self.led_col_list = collist
  #   self.num_of_led_row = len(rowlist)
  #   self.num_of_led_col = len(collist)

  def get_led_row_list(self):
    return self.led_row_list

  def get_led_col_list(self):
    return self.led_col_list

  def get_num_of_led_row(self):
    return self.num_of_led_row

  def get_num_of_led_col(self):
    return self.num_of_led_col

  def runMode(self, strip):
    isplottable = True
    plottraillength = 0
    self.lightsArray = []    
    if (int(self.mode) == 0):
      # print("0iss")
      plottraillength = 35
      for i in lightIss(self.ledcoords):
        self.lightsArray.append(i)
    elif (int(self.mode) == 1):
      # print("1sun")
      for i in lightSun(self.ledcoords):
        self.lightsArray.append(i)
    elif (int(self.mode) == 2):
      # print("2moon")
      for i in lightMoon(self.ledcoords):
        self.lightsArray.append(i)
    elif (int(self.mode) == 3):
      # print("3all")
      for i in lightSun(self.ledcoords):
        self.lightsArray.append(i)
      for i in lightMoon(self.ledcoords):
        self.lightsArray.append(i)
      for i in lightIss(self.ledcoords):
        self.lightsArray.append(i)
    elif (int(self.mode) == 4):
      isplottable = False
      rainbowColumnCycle(strip, getColumnArray(self.ledcoords))

    colorSetAll(strip, Color(0,0,0))
    for i in self.lightsArray:
      logging.debug(i)
      strip.setPixelColor(i[0], i[1])

    if logging.getLogger().getEffectiveLevel()==(logging.DEBUG) and isplottable:
      # plot(self, self.lightsArray, self.ledcoords, plottraillength)
      plot(self, plottraillength)
    protectionShow(strip)
    # print(lightsArray)                

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
    dist = calcDist(lat, lon, y, x)
    if dist < distance:
      lights.append(pointArray.index(i))
  return lights

def getClosestPoint(lat, lon, pointArray):
  point = 0
  minDist = 100000
  for i in pointArray:
    # print(i)
    pointlat = i[1]
    pointlon = i[0]
    # print (lat, lon, x, y)

    # convert x to a longintude (-180 to 180) NOT (0 to 360)
    #Longitude can be between 0~360 (long3) and -180~180 (long1)
    # pointlong3 = pointlon
    # pointlong1 = (pointlong3 + 180) % 360 - 180

    dist = calcDist(lat, lon, pointlat, pointlon)
    # print (dist)
    # print("{},{},{}".format(x,y,round(dist,0)))
    if dist < minDist:
      point = pointArray.index(i)
#      coord = str(x)+","+str(y)
      minDist = dist
      # print (point, dist)
#       print (lat, lon, x, y)
  # pointlong1 = (pointArray[point][0] + 180) % 360 - 180
  logging.debug("closest point is: {}: ({}, {}) with distance of: {}".format(point, pointArray[point][1], pointArray[point][0], minDist))
  # logging.debug("Point {} has a calculated longitude of {}".format(point, pointlong1))
  
#   print (lat,lon,pointArray[point][0], pointArray[point][1])
  # print (point, pointArray[point], minDist)
  
  return point

def getClosestPoints(lat, lon, pointArray, amount):
  tempPointArray = pointArray.copy()
  topDistList = []
  for y in range(amount):
    point = 0
    minDist = 100000
    for i in tempPointArray:
      pointlat = i[1]
      pointlon = i[0]
      dist = calcDist(lat, lon, pointlat, pointlon)
      # print(x,y,dist)
      if dist < minDist:
        point = tempPointArray.index(i)
        coord = str(pointlon)+","+str(pointlon)
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
#   R = (ephem.earth_radius/1000)
#   lat1 = radians(lat1)
#   lon1 = radians(lon1)
#   lat2 = radians(lat2)
#   lon2 = radians(lon2)
#   dlon = (abs(lon2 - lon1))
#   dlat = (abs(lat2 - lat1))
# #   print (dlon, dlat)
#   a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#   c = 2 * atan2(sqrt(a), sqrt(1 - a))
#   distance = R * c

  # print(gdistance.distance((lat1,lon1), (lat2,lon2)).km)
  # print(distance)

  return gdistance.distance((lat1,lon1), (lat2,lon2)).km

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

class TimeoutExpired(Exception):
  pass

def input_with_timeout(prompt, timeout):
  sys.stdout.write(prompt)
  sys.stdout.flush()
  ready, _, _ = select.select([sys.stdin], [],[], timeout)
  if ready:
    return sys.stdin.readline().rstrip('\n') # expect stdin to be line-buffered
  raise TimeoutExpired

def chkChangeMode(timer, currMode):
  try:
    answer = input_with_timeout("Mode:", timer)
  except TimeoutExpired:
    logging.debug("Cycle Complete: Mode staying at %d" % int(currMode))
    return currMode
  else:
    if (int(answer) >= 0) and (int(answer) <= 4):
      currMode = answer
    logging.info('Mode updated to %s' % int(currMode))
    return currMode

def changeMode(currMode):
  #call this when button press
  modeList = [1,2,3,4,0]
  currMode = modeList[currMode]
  return currMode
  
# def createHeightArray(pointArray):
#   heightArray = []
#   for i in pointArray:
#     heightArray.append(i[1])
#   return heightArray

def systemOn(LightArray, strip):
  scrollup(strip, LightArray.getLedCoords())

def systemOff(LightArray, strip):
  LightArray.getLedCoords()
  scrolldown(strip, LightArray.getLedCoords())

# def getColumnArray(pointArray):
#   #get array of points with each (point,column)
#   columns = [0,11.25,22.5,33.75,45,56.25,67.5,78.75,90,101.25,112.5,123.75,135,146.25,157.5,168.75,180,191.25,202.5,213.75,225,236.25,247.5,258.75,270,281.25,292.5,303.75,315,326.25,337.5,348.75]
#   columnArray = []
#   for j in pointArray:
#     columnArray.append((pointArray.index(j), columns.index(j[1])))
#   return columnArray
