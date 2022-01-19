from gpiozero import Button
from systemcontroller import sysshutdown
import issglobeconfig as cfg
import logging

class btncontroller:
  def __init__(self, lightarr):
    self.lightarray = lightarr
    # modeButton = Button(cfg.mode_BTN_PIN, hold_time=5) #bounce_time=.5, hold_time=7)
    logging.info('watching buttons..')
    # modeButton.when_pressed = self.modeButtonPressed
    # modeButton.when_held = self.lightarray.systemOff

  def modeButtonPressed(self):
    logging.info('mode button pressed')
    self.lightarray.changeMode()

  def modeButtonHeld(self):
    logging.info("shutting down")
    self.lightarray.systemOff()
    self.lightarray.wipecolorstrip()
    sysshutdown()
