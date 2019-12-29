# from ledcontrol import systemOn
from lightarray import runMode, systemOn, systemOff, currMode, changeMode
from ledcontrol import colorAll
from gpiozero import Button
from neopixel import Color, Adafruit_NeoPixel
import argparse
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG)

# LED strip configuration:
LED_COUNT      = 400      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 150     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

BTN_PIN = 23

global currMode

def modeButtonPressed():
    global currMode
    currMode = changeMode(currMode)

def modeButtonHeld():
    print("shutting down")
    systemOff(strip)
    colorAll(strip, Color(0, 0, 0))

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--clear', action='store_true', help='clear the display on exit')
 #   parser.add_argument(
 #       '-v', '--Verbose', action='store_true' help="when set will output logger ")
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # # Intialize the library (must be called once before other functions).
    strip.begin()

    modeButton = Button(BTN_PIN, bounce_time=.5, hold_time=7)

#    logging.Logger.setLevel("WARNING")

    print ('Press Ctrl-C to quit.')
    if not args.clear:
      print('Use "-c" argument to clear LEDs on exit')

    try:
        systemOn(strip)
        modeButton.when_pressed = modeButtonPressed
        modeButton.when_held = modeButtonHeld

        while True:
            currMode = runMode(currMode, strip)
            sleep(5)

    except KeyboardInterrupt:
        if args.clear:
            modeButtonHeld()