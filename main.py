# from ledcontrol import systemOn
from lightarray import runMode, chkChangeMode, systemOn, systemOff, currMode, changeMode
from ledcontrol import colorWipe, colorSet, colorSetAll
from gpiozero import Button
# from neopixel import *
import argparse
from colorzero import Color
import logging

logging.basicConfig(level=logging.INFO)

maxLedOn = 100  #max number of leds that should be on to stay under amp rating


class strip:
    colorArray = []

    def __init__(self):
        for i in range(400):
            self.colorArray.append((i, Color(
                0,
                0,
                0,
            )))

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


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    # strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # # Intialize the library (must be called once before other functions).
    strip = strip()
    strip.begin()

    # print ('Press Ctrl-C to quit.')
    # if not args.clear:
    #   print('Use "-c" argument to clear LEDs on exit')

    try:
        systemOn(strip)
        # colorSet(strip, Color(255, 0, 0), 5)
        # colorSet(strip, Color(255, 0, 0), 6)
        # colorSetAll(strip, Color(0,0,0))

        while True:
            currMode = runMode(currMode, strip)
            currMode = chkChangeMode(10, currMode)
        # while True:
        # print ('Color wipe animations.')
        # colorWipe(strip, Color(255, 0, 0))  # Red wipe
        # colorWipe(strip, Color(0, 255, 0))  # Blue wipe
        # colorWipe(strip, Color(0, 0, 255))  # Green wipe
        # print ('Theater chase animations.')
        # theaterChase(strip, Color(127, 127, 127))  # White theater chase
        # theaterChase(strip, Color(127,   0,   0))  # Red theater chase
        # theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
