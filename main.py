# from ledcontrol import systemOn
from lightarray import runMode, chkChangeMode, systemOn, systemOff, currMode, changeMode
from ledcontrol import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
from gpiozero import Button
from neopixel import *
import argparse

maxLedOn = 100 #max number of leds that should be on to stay under amp rating

# Main program logic follows:
if __name__ == '__main__':
  # Process arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
  args = parser.parse_args()

  # Create NeoPixel object with appropriate configuration.
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  # Intialize the library (must be called once before other functions).
  strip.begin()

  print ('Press Ctrl-C to quit.')
  if not args.clear:
      print('Use "-c" argument to clear LEDs on exit')

  try:

    while True:
      print ('Color wipe animations.')
      colorWipe(strip, Color(255, 0, 0))  # Red wipe
      colorWipe(strip, Color(0, 255, 0))  # Blue wipe
      colorWipe(strip, Color(0, 0, 255))  # Green wipe
      print ('Theater chase animations.')
      theaterChase(strip, Color(127, 127, 127))  # White theater chase
      theaterChase(strip, Color(127,   0,   0))  # Red theater chase
      theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase

    except KeyboardInterrupt:
      if args.clear:
        colorWipe(strip, Color(0,0,0), 10)