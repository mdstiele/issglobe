from gpiozero import Button
from systemcontroller import sysshutdown
import issglobeconfig as cfg

class btncontroller:
  def __init__(self, lightarr):
    self.lightarray = lightarr
    # modeButton = Button(cfg.mode_BTN_PIN, hold_time=5) #bounce_time=.5, hold_time=7)
    print('watching buttons..')
    # modeButton.when_pressed = self.modeButtonPressed
    # modeButton.when_held = self.lightarray.systemOff

  def modeButtonPressed(self):
    print('mode button pressed')
    self.lightarray.changeMode()

  def modeButtonHeld(self):
    print("shutting down")
    self.lightarray.systemOff()
    self.lightarray.wipecolorstrip()
    sysshutdown()
