from collections import deque
trail = deque()

def plot(colorArray, pointArray):
  rows = 30
  cols = 40
  rowList = [76.5,71.4,66.3,61.2,56.1,51,45.9,40.8,35.7,30.6,25.5,20.4,15.3,10.2,5.1,0,-5.1,-10.2,-15.3,-20.4,-25.5,-30.6,-35.7,-40.8,-45.9,-51,-56.1,-61.2,-66.3,-71.4,-76.5]
  colList = [180,191.25,202.5,213.75,225,236.25,247.5,258.75,270,281.25,292.5,303.75,315,326.25,337.5,348.75,0,11.25,22.5,33.75,45,56.25,67.5,78.75,90,101.25,112.5,123.75,135,146.25,157.5,168.75]

  # print(pointArray[lightArray[0][0]] in pointArray)

  #apends just the led number from color array to lightarray
  #example
  #[(219, <Color html='#ff0000' rgb=(1, 0, 0)>)]  ->  [219]
  lightArray = []
  for k in colorArray:
    lightArray.append(k[0])

  print(lightArray)
  
  string = ""
  for i in rowList:
    # string = string + str(rowList.index(i)).ljust(2, ' ') + " |" 
    string = string + str(i).ljust(5, ' ') + " |" 
    for j in colList:
      light = False
      old = False
      map = False
      # print(pointArray.index((i,j) in lightArray)
      # print((j,i))
      if ((i,j) in pointArray):
        if(pointArray.index((i,j)) in lightArray):
          light = True
        elif(pointArray.index((i,j)) in trail):
          old = True
        else:
          map = True
      

      if i==0:
        string= string + "  -  "
      elif(light):
        string = string + "  O  "
      elif(old):
        string = string + "  +  "
      elif(map):
        string = string + "  .  "
      else:
        string = string + "     "
    string = string + "|"
    string = string + "\n"
  string = string + ">"
  print("\r" + string, end = ">")

    #this only works if lightray is single int
  if len(lightArray) == 1:
    led = lightArray.pop()
    if led not in trail:
      trail.append(led)
  while len(trail)>20:
    trail.popleft()
  print(trail)

# if __name__ == '__main__':
  
#   # print(pointArray)
#   lightArray = [(283, "Color"),(120, "Color")]
#   plot(lightArray)