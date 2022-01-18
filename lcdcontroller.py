#!/usr/bin/env python

import time
import pi_ic2_lib

mylcd = pi_ic2_lib.lcd()

def showclock():
  while True:
    mylcd.lcd_display_string(time.strftime('%I:%M:%S %p'), 3)
    mylcd.lcd_display_string(time.strftime('%a %b %d, 20%y'), 4)

def showcustomchar():
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
    mylcd.lcd_load_custom_chars(fontdata1)