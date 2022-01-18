#!/usr/bin/env python

import time
import pi_ic2_lib
from threading import Thread
from time import sleep

class lcdclock:
  def __init__(self):
    self._running = True
    self.mylcd = pi_ic2_lib.lcd()

  def terminate(self):
    self._running = False
    sleep(.5)
    self.mylcd.lcd_clear()

  def showclock(self):
    while self._running:
      self.mylcd.lcd_display_string('{:^20}'.format(time.strftime('%I:%M:%S %p')), 3)
      self.mylcd.lcd_display_string('{:^20}'.format(time.strftime('%a %b %d, 20%y')), 4)

  def loadcustomchar(self):
    # let's define a custom icon, consisting of 6 individual characters
    # 3 chars in the first row and 3 chars in the second row
    fontdata1 = [
      # Char 0 - Upper-left
      [ 0x00, 0x00, 0x01, 0x03, 0x07, 0x07, 0x0F, 0x0B ],
      # Char 1 - Upper-middle
      [ 0x00, 0x0F, 0x17, 0x1B, 0x18, 0x10, 0x00, 0x00 ],
      # Char 2 - Upper-right
      [ 0x00, 0x00, 0x18, 0x0C, 0x16, 0x0E, 0x0F, 0x1D ],
      # Char 3 - Lower-left
      [ 0x09, 0x0B, 0x07, 0x07, 0x03, 0x01, 0x00, 0x00 ],
      # Char 4 - Lower-middle
      [ 0x01, 0x13, 0x19, 0x1C, 0x18, 0x18, 0x0F, 0x00 ],
      # Char 5 - Lower-right
      [ 0x19, 0x1D, 0x1E, 0x1E, 0x1C, 0x18, 0x00, 0x00 ],
    ]
    # Load logo chars (fontdata1)
    self.mylcd.lcd_load_custom_chars(fontdata1)

  def showcustomchar(self):
    self.mylcd.lcd_write(0x80)
    self.mylcd.lcd_write_char(0)
    self.mylcd.lcd_write_char(1)
    self.mylcd.lcd_write_char(2)
    self.mylcd.lcd_write(0xC0)
    self.mylcd.lcd_write_char(3)
    self.mylcd.lcd_write_char(4)
    self.mylcd.lcd_write_char(5)

if __name__ == '__main__':
  try:
    lcdclk = lcdclock()
    lcdclk.loadcustomchar()
    lcdclkthread = Thread(target=lcdclk.showclock)
    lcdclkthread.start()
    lcdclkthread.join()

  except KeyboardInterrupt:
    lcdclk.terminate()
