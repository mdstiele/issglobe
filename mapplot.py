from collections import deque
import logging
# from lightarray import Lightarray
pastpoints = deque()
landCoordsDir = "ledcoords_land.txt"
plotwidth = 7

def getLandCoords():
  f2 = open("ledcoords_land.txt", "r")
  flines2 = f2.read().split("\n")
  outputList2 = []
  for i in flines2:
    outputList2.append(eval(i))
  return outputList2 #0-399

class plots(object):
    plot_list = []

    def __init__(self, name, symbol):
        self.plot_list.append(self)
        self.name = name
        self.lightarray = []
        self.symbol = str(symbol)

    def get_name(self):
      return self.name

    def set_lightarray(self, lightarray):
      self.lightarray = lightarray

    def get_lightarray(self):
      return self.lightarray

# self.lightsArray, self.ledcoords,
# def plot(colorArray, pointArray, traillength=0):
def plot(lightarray, traillength=0):
  logging.debug("Showing Mapplot")
  rowList = lightarray.get_led_row_list()
  colList = sorted(lightarray.get_led_col_list())
  pointArray = lightarray.getLedCoords()
  # print(rowList)
  # rowList = [76.5,71.4,66.3,61.2,56.1,51,45.9,40.8,35.7,30.6,25.5,20.4,15.3,10.2,5.1,0,-5.1,-10.2,-15.3,-20.4,-25.5,-30.6,-35.7,-40.8,-45.9,-51,-56.1,-61.2,-66.3,-71.4,-76.5]
  # colList = [180,191.25,202.5,213.75,225,236.25,247.5,258.75,270,281.25,292.5,303.75,315,326.25,337.5,348.75,0,11.25,22.5,33.75,45,56.25,67.5,78.75,90,101.25,112.5,123.75,135,146.25,157.5,168.75]
  LandBool = []
  LandBool = getLandCoords()

  # print(pointArray[lightArray[0][0]] in pointArray)

  #apends just the led number from color array to plotlightarray
  #example
  #[(219, <Color html='#ff0000' rgb=(1, 0, 0)>)]  ->  [219]
  plotisslightArray = []
  plotsunlightArray = []
  plotmoonlightArray = []
  # for k in lightarray.get_lights_array():
  #   plotlightArray.append(k[0])
  for k in lightarray.get_iss_lights_array():
    plotisslightArray.append(k[0])

  for l in lightarray.get_sun_lights_array():
    plotsunlightArray.append(l[0])  

  for m in lightarray.get_moon_lights_array():
    plotmoonlightArray.append(m[0])

  string = ""
  for i in rowList:
    # string = string + str(rowList.index(i)).ljust(2, ' ') + " |" 
    string = string + str(i).ljust(plotwidth, ' ') + " |" 
    for j in colList:
      iss = sun = moon = trail = map = False
      land = False
      # print(pointArray.index((i,j) in lightArray)
      # print((j,i))
      if ((j,i) in pointArray):
        # print(pointArray.index((j,i)))
        # if(pointArray.index((j,i)) in plotlightArray):
        #   light = True
        if(pointArray.index((j,i)) in plotisslightArray):
          iss = True
        elif(pointArray.index((j,i)) in plotmoonlightArray):
          moon = True
        elif(pointArray.index((j,i)) in plotsunlightArray):
          sun = True
        elif((traillength > 0) and pointArray.index((j,i)) in pastpoints):
          trail = True
          # print(LandBool[pointArray.index((i,j))][2])
        elif(LandBool[pointArray.index((j,i))]):
          # map = True
          land = True
          # landcoords[LandBool.index((i,j))]
        else:
          map = True
      
      
      if(iss):
        string = string + " I "
      elif(trail):
        string = string + " T "
      elif(moon):
        string = string + " M "
      elif(sun):
        string = string + " s "
      elif i==0:
        string= string + " - "
      elif(land):#map):
        string = string + " . "
      else:
        string = string + "   "
    string = string + "|"
    string = string + "\n"
  string = string + ">"
  print("\r" + string, end = ">")

  if (traillength > 0):
    #this only works if lightray is single int
    if len(plotisslightArray) == 1:
      led = plotisslightArray.pop()
      if led not in pastpoints:
        pastpoints.append(led)
    while len(pastpoints)>traillength:
      pastpoints.popleft()

# if __name__ == '__main__':
  
#   # print(pointArray)
#   lightArray = [(283, "Color"),(120, "Color")]
#   plot(lightArray)