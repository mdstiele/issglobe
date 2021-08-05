Info:
name = "issglobe"
version = "0.1.0"
description = ""
authors = ["Michael Stieler <mdstieler@gmail.com>"]

Dependencies:
python = "^3.7"
ephem = "^3.7"

pinout (RPi0w)
  4 power+ in
  6 power- in
  8 (GPIO14) Pi status led
  12 (GPIO 18) led strip data
  16 (GPIO 23) mode switch button
  ? Mode led
  ? wps button

Todo:
  1.put button on its own thread
  2.clean up all crap
  3.only check for new tle after a certain amount of time
  4. status led (for running and shutdown) as shown here: https://howchoo.com/g/ytzjyzy4m2e/build-a-simple-raspberry-pi-led-power-status-indicator#methods-for-adding-pi-led-status-indicators
  5. add mode led
  6. add wps button? https://www.raspberrypi.org/forums/viewtopic.php?t=226333
  7. wifi status led or change other led to blink?

Done:
  1.change wheel color program to align vertical colums in color
  2.fix calc dist command
  3.dont set curr mode in run mode
  4.fix logger to not show unless wanted
