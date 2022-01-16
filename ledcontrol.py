from neopixel import Color
#from neopixel_mock_ms import Color
import time
import logging
# from colorzero import Color as Color2

# # LED strip configuration:
# LED_COUNT      = 16      # Number of LED pixels.
# LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
# #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
# LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
# LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53                

maxLedOn = 200 #max number of leds that should be on to stay under amp rating

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
  """Wipe color across display a pixel at a time."""
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, color)
    protectionShow(strip)
    time.sleep(wait_ms/1000.0)

def colorSetAll(strip, color):
  """Set color to each pixel all at same time."""
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, color)

def colorAll(strip, color):
  """Set color to each pixel all at same time."""
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, color)
  protectionShow(strip)

def colorSet(strip, color, led):
  """Set color to specific led pixel"""
  strip.setPixelColor(led, color)
  protectionShow(strip)

def scrollup(strip, pointArray, color=Color(0, 0, 255), wait_ms=1):
  for j in range(-70, 90, 20):
    for q in pointArray:
      p=q[1]
      if ((j-20) <= p <= j):
        strip.setPixelColor(pointArray.index(q), color)
      else:
        strip.setPixelColor(pointArray.index(q), Color(0,0,0))
    protectionShow(strip)
    logging.debug("scrollup cycle: {}".format(j))

def scrolldown(strip, pointArray, color=Color(255, 0, 0), wait_ms=50):
  for j in range(90, -80, -10):
    for q in pointArray:
      p=q[0]
      if ((j-10) <= p <= j):
        # showArray.append((pointArray.index(q), color))
        strip.setPixelColor(pointArray.index(q), color)
      else:
        strip.setPixelColor(pointArray.index(q), Color(0,0,0))
    protectionShow(strip)
    time.sleep(wait_ms/1000.0)
    logging.debug("scrolldown cycle: {}".format(j))

def theaterChase(strip, color, wait_ms=50, iterations=10):
  """Movie theater light style chaser animation."""
  for j in range(iterations):
    for q in range(3):
      for i in range(0, strip.numPixels(), 3):
        strip.setPixelColor(i+q, color)
      protectionShow(strip)
      time.sleep(wait_ms/1000.0)
      for i in range(0, strip.numPixels(), 3):
        strip.setPixelColor(i+q, 0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def protectionShow(strip):
  #switch to import and use lenth of strip
  #use strip.getpixels()
  #count non 0 colors
  count = 0
  #for i in strip.getPixels():
    # if (i[1] != Color(0,0,0)): #colorzero
      # count += 1
   # if (i != Color(0,0,0)): #neopixel
    #  count += 1
  for i in range(strip.numPixels()):
    if (strip.getPixelColor(i) != Color(0,0,0)):
      count += 1

  if count <= maxLedOn:
    logging.info("Protection show: {} LEDs on".format(count))
    strip.show()
  else:
    logging.error("{} LEDs is over threshold, overload prevention activated".format(count))
    #do tests to see if can turn brightness down

def rainbowColumnCycle(strip, columnArray, wait_ms=20, iterations=5):
  numColumns = 32 #32 columns change to use calculated col num
  for j in range(256*iterations):
    for i in range(len(columnArray)):
      strip.setPixelColor(i,wheel((int(columnArray[i][1] * 256 / numColumns) + j) & 255))
    strip.show()
    time.sleep(wait_ms/1000.0)
