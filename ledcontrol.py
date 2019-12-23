# from neopixel import *
# import argparse
import time

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
maxLedOn = 100 #max number of leds that should be on to stay under amp rating

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
  """Wipe color across display a pixel at a time."""
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, color)
    protectionShow(strip)
    time.sleep(wait_ms/1000.0)

def colorSet(strip, color, led):
  """Set color to specific led pixel"""
  strip.setPixelColor(led, color)
  protectionShow(strip)

def scrollup(pointArray, color="Color(0, 0, 255)", wait_ms=50):
  for j in range(-80, 90, 10):
    showArray = []
    for q in pointArray:
      p=q[1]
      if ((j-10) <= p <= j):
        showArray.append((pointArray.index(q), color))
        # print(pointArray.index(q), q, color)
        # strip.setPixelColor(heightArray.index(q), color)
      else:
        showArray.append((pointArray.index(q), "Color(0,0,0)"))
        # strip.setPixelColor(heightArray.index(q), color(0,0,0))
    # strip.show()
    protectionShow(showArray)
    print("cycle", j)
    time.sleep(wait_ms/1000.0)

def scrolldown(pointArray, color="Color(255, 0, 0)", wait_ms=50):
  for j in range(90, -80, -10):
    showArray = []
    for q in pointArray:
      p=q[1]
      if ((j-10) <= p <= j):
        showArray.append((pointArray.index(q), color))
        # print(pointArray.index(q), q, color)
        # strip.setPixelColor(heightArray.index(q), color)
      else:
        showArray.append((pointArray.index(q), "Color(0,0,0)"))
        # strip.setPixelColor(heightArray.index(q), color(0,0,0))
    # strip.show()
    protectionShow(showArray)
    time.sleep(wait_ms/1000.0)

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

def protectionShow(showArray):
  #switch to import and use lenth of strip
  #use strip.getpixels()
  #count non 0 colors
  count = 0
  for i in showArray:
    if (i[1] != "Color(0,0,0)"):
      count += 1
      # strip.setPixelColor(i, color)
  print(count)

  if count <= maxLedOn:
    print("show")
    #strip.show
  else:
    print("Error: Too many LEDs, overload prevention activated")
    #do tests to see if can turn brightness down
