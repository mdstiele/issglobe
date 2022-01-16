Info:
name = "issglobe"
version = "0.1.0"
description = ""
authors = ["Michael Stieler <mdstieler@gmail.com>"]

Dependencies:
python = "^3.8"
ephem = "^4.0.0"
gpiozero = "^1.6.2"
rpi-ws281x = "^4.3.0"
geopy = "^2.2.0"

Optional:
global-land-mask = "^1.0.0"

default pinout (RPi0w)
  4 power+ in
  6 power- in
  8 (GPIO14) Pi status led
  12 (GPIO 18) led strip data
  16 (GPIO 23) mode switch button
  ? Mode led
  ? wps button