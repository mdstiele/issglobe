# from ledcontrol import systemOn
from lightarray import runMode, chkChangeMode, systemOn, systemOff, currMode, changeMode
from ledcontrol import colorWipe, colorAll
# from gpiozero import Button, Device
# from gpiozero.pins.mock import MockFactory
from neopixel_mock import Color, Adafruit_NeoPixel
import argparse
# from colorzero import Color
import logging
from time import sleep

#mock devices
# Device.pin_factory = MockFactory()
logging.basicConfig(level=logging.DEBUG)

maxLedOn = 100  #max number of leds that should be on to stay under amp rating


# import only system from os
from os import system, name
# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

#THIS IS MY MADE MOCK STUFF
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


# LED strip configuration:
LED_COUNT      = 400      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 150     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# BTN_PIN = 23

# global currMode

# def modeButtonPressed():
#     global currMode
#     currMode = changeMode(currMode)

# def modeButtonHeld():
#     print("shutting down")
#     systemOff(strip)
#     colorAll(strip, Color(0, 0, 0))

# Main program logic follows:
if __name__ == '__main__':
    # # Process arguments
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '-c', '--clear', action='store_true', help='clear the display on exit')
    # parser.add_argument(
    #     '-v', '--verbose', action='store_true', help='when set will sre logger to DEBUG otherwise will be WARNING')
    # args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    # strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip = strip()
    strip.begin()

    # # modeButton = Button(BTN_PIN, bounce_time=.5, hold_time=7)

    # print ('Press Ctrl-C to quit.')
    # if not args.clear:
    #   print('Use "-c" argument to clear LEDs on exit')
    
    # if args.verbose:
    #   logging.basicConfig(level=logging.DEBUG)
    # else:
    #   logging.basicConfig(level=logging.WARNING)

    # try:
        # systemOn(strip)
        # modeButton.when_pressed = modeButtonPressed
        # modeButton.when_held = modeButtonHeld

    while True:
        clear()
        currMode = runMode(currMode, strip)
        sleep(5)

    # except KeyboardInterrupt:
    #     if args.clear:
    #         # modeButtonHeld()
    #         colorWipe(strip, Color(0, 0, 0), 10)







# from lightarray import getLedCoords, lightMoon, calcDist, getColumnArray #runMode, systemOn, systemOff, currMode,
# from ledcontrol import rainbowColumnCycle
# import logging
# from time import sleep


# import threading
# import time
# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BOARD)

# class Button(threading.Thread):
#     def __init__(self, channel):
#         threading.Thread.__init__(self)
#         self._pressed = False
#         self.channel = channel
#         GPIO.setup(self.channel, GPIO.IN)
#         self.deamon = True
#         self.start()

#     def run(self):
#         previous = None
#         while 1:
#             current = GPIO.input(self.channel)
#             time.sleep(0.01)

#             if current is False and previous is True:
#                 self._pressed = True

#                 while self._pressed:
#                     time.sleep(0.05)

#             previous = current

#     def onButtonPress():
#         print("btn presdsed")

# button = Button(36)

# while True:
#     name = input('Enter a Name:')

#     if name.upper() == ('Q'):
#         break
#     print('hello', name)

#     if button.pressed():
#         onButtonPress()



# if __name__ == '__main__':
 
#   logging.basicConfig(level=logging.INFO)
#   # while True:
#   # points = lightMoon(led_coords)
#   # for i in points:
#   #     print (led_coords[i[0]][0], led_coords[i[0]][1])
#     # print (led_coords[point[0][0]])
#     # if last != point:
#     #   last = point
#     # print (led_coords[point[0][0]])
#     # sleep(5)