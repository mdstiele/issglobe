#import ephem
from lightarray import Lightarray
from ledcontrol import * #colorWipe#, colorAll, systemOn
from gpiozero import Button, Device
# from gpiozero.pins.mock import MockFactory
from neopixel import *
# from neopixel_mock_ms import strip, Color
import argparse
import logging
from time import sleep
from os import system, name
from subprocess import check_call
import lcd1602 as LCD

#mock devices
# Device.pin_factory = MockFactory()
logging.basicConfig(level=logging.INFO)#, force = True)
refreshseconds = 5
maxLedOn = 100  #max number of leds that should be on to stay under amp rating

# LED strip configuration:
LED_COUNT      = 400      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 150     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# LCD pin configuration
# #lcdk = gnd(p39)
# #lcdA = 3v3(p17)
# lcdD7 = gpio26(p37)
# lcdD6 = gpio19(p35)
# lcdD5 = gpio13(p33)
# lcdD4 = gpio6(p31)
# lcdE = gpio5(p29)
# #lcdR/W = gnd(p25)
# lcdRS = gpio11(p23)
# #lcdov = pot mid
# #lcdVcc = 5v(p4)
# #lcdVss = gnd(p34)

#button gpiozero settings
BTN_PIN = 23

#global currMode
#global lcd

def modeButtonPressed():
    print('mode button pressed')
#     global currMode
#    currMode = changeMode(currMode)
    lightarray.changeMode()

def modeButtonHeld():
    print("shutting down")
    lightarray.systemOff()
    colorAll(strip, Color(0, 0, 0))
    check_call(['sudo', 'poweroff'])

#Clear the console
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
         '-c', '--clear', action='store_true', help='clear the led display on exit, otherwise it will hold the last colors set')
    parser.add_argument(
         '-v', '--verbose', action='count', default = 1, help='each v increases the logger level. default is WARNING, "-v" is INFO, "-vv" is DEBUG')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    #strip = strip()
    strip.begin()
    lightarray = Lightarray(strip)

    modeButton = Button(BTN_PIN, hold_time=5) #bounce_time=.5, hold_time=7)

    print ('Press Ctrl-C to quit.')
    if not args.clear:
    	print('Use "-c" argument to clear LEDs on exit')
    sleep(5)
    args.verbose = 40 - (10*args.verbose) if args.verbose > 0 else 0
    logging.basicConfig(level=args.verbose, force=True, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    #if args.verbosei:
    #    logging.basicConfig(level=logging.INFO, force=True)
    #if args.verbosed:
    #    logging.basicConfig(level=logging.DEBUG, force=True)

    try:
        #initialize the LCD and set welcome message
        lcd = LCD.LCD()
        lightarray.setlcd(lcd)
        lcd.clear()
        lcd.message("Welcome to --->\n  IssGlobe v0.1")

        lightarray.systemOn()
        #sleep(10)
        print('watching buttons..')
        modeButton.when_pressed = lightarray.changeMode #modeButtonPressed
        modeButton.when_held = lightarray.systemOff

        while True:
#            clear()
            lightarray.runMultiMode(strip)
            #sleep(refreshseconds)

    except KeyboardInterrupt:
        if args.clear:
            # modeButtonHeld()
            print("shutdown")
            colorWipe(strip, Color(0, 0, 0), 10) #call the lightarray clear or ledcontrol clear
            lcd.clear()
            lcd.destroy()

	# line0 = " hello,world!"
	# line1 = "SunFounder"

	# lcd.clear()
	# lcd.message("Welcome to --->\n  SunFounder")
	# sleep(3)

	# msg = "%s\n%s" % (line0, line1)
	# while True:
	# 	lcd.begin(0, 2)
	# 	lcd.clear()
	# 	for i in range(0, len(line0)):
	# 		lcd.setCursor(i, 0)
	# 		lcd.message(line0[i])
	# 		sleep(0.1)
	# 	for i in range(0, len(line1)):
	# 		lcd.setCursor(i, 1)
	# 		lcd.message(line1[i])
	# 		sleep(0.1)
	# 	sleep(1)
