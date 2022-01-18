from lightarraycontroller import Lightarray
from neopixel import Adafruit_NeoPixel
import argparse
import logging
#from time import sleep
import lcdcontroller as LCD
from buttoncontroller import btncontroller
import issglobeconfig as cfg

logging.basicConfig(level=logging.INFO) #, force = True)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
         '-c', '--clear', action='store_true', help='clear the led display on exit, otherwise it will hold the last colors set')
    parser.add_argument(
         '-v', '--verbose', action='count', default = 1, help='each v increases the logger level. default is WARNING, "-v" is INFO, "-vv" is DEBUG')
    args = parser.parse_args()

    args.verbose = 40 - (10*args.verbose) if args.verbose > 0 else 0
    logging.basicConfig(level=args.verbose, force=True, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    print ('Press Ctrl-C to quit.')
    if not args.clear:
    	print('Use "-c" argument to clear LEDs on exit')

    #if args.verbosei:
    #    logging.basicConfig(level=logging.INFO, force=True)
    #if args.verbosed:
    #    logging.basicConfig(level=logging.DEBUG, force=True)

    try:
        #initialize the neopixel strip
        strip = Adafruit_NeoPixel(cfg.LED_COUNT, cfg.LED_PIN, cfg.LED_FREQ_HZ, cfg.LED_DMA, cfg.LED_INVERT, cfg.LED_BRIGHTNESS, cfg.LED_CHANNEL)  # Create NeoPixel object with appropriate configuration.
        strip.begin() # Intialize the library (must be called once before other functions).

        #initialize the lightarray
        lightarray = Lightarray(strip)

        #initialize the LCD and set welcome message
        lcd = LCD.lcdclock()
        lightarray.setlcd(lcd)
        #lcd.clear()
        lcd.printwelcome()

        lightarray.systemOn()
        #sleep(10)

        #initialize the button controller
        btncontroller = btncontroller(lightarray)

        while True:
#            clear()
            lightarray.runMultiMode()
            #sleep(refreshseconds)

    except KeyboardInterrupt:
        if args.clear:
            # modeButtonHeld()
            print("\n shutdown")
            lightarray.wipecolorstrip()
            lcd.terminate()
            #lcd.destroy()




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
