#THIS IS MY MADE MOCK STUFF

#FROM NEOPIXEL
def Color(red, green, blue, white=0):
  """Convert the provided red, green, blue color to a 24-bit color value.
  Each color component should be a value 0-255 where 0 is the lowest intensity
  and 255 is the highest intensity.
  """
  return (white << 24) | (red << 16) | (green << 8) | blue

class strip:
    colorArray = []

    def __init__(self):
        for i in range(400):
            self.colorArray.append((i, Color(0, 0, 0)))

    def begin(self):
        return

    def setPixelColor(self, index, Color):
        for i in range(0, 399):
            arrayPoint = self.colorArray[i]
            arrayIndex = arrayPoint[0]
            if arrayIndex == index:
                del self.colorArray[i]
        self.colorArray.append((index, Color))
        
    def numPixels(self):
        return 400

    def getPixels(self):
        return self.colorArray

    def show(self):
        return