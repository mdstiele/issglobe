from neopixel_mock_ms import Color
import ephem
import math

# configuration file for use with the issglobe project

# LED strip configuration:
LED_COUNT      = 400      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 150     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

maxLedOn = 200  #max number of leds that should be on to stay under amp rating

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

mode_BTN_PIN = 23

isrunningonreplit = True

# set the Trackable objects here and set their settings
degrees_per_radian = 180.0 / math.pi
sun = ephem.Sun()
moon = ephem.Moon()
greenwich = ephem.Observer()
greenwich.lat = "0"
greenwich.lon = "0"
sunLightRadius = ephem.earth_radius/1000 * 1.5 #earth radius should mean about 50% coverage
moonLightRadius = (ephem.earth_radius/1000)*.33 #1/3 earth radius
sunLightColor = Color(255,255,200) #yellow white
moonLightColor = Color(255,0,255) #light blue
issLightColor = Color(0,255,0) #red
totalNumLed = 40 #total number of leds on system
statusLed = 41 #number in chain of the status led
currMode = 0 #the current mode, starts at 0
defaultMode = 0 #defualt mode when the system starts

isstledir = "isstle.txt"
ledCoordsDir = "ledcoords.txt"#"/home/pi/issglobe/ledcoords.txt"