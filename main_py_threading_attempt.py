# from lightarray import getLedCoords, lightMoon, calcDist, getColumnArray #runMode, systemOn, systemOff, currMode,
# from ledcontrol import rainbowColumnCycle
# import logging
# from time import sleep


# import threading
# import time
# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BOARD)

# class Button(threading.Thread):
#     def __init__(self, channel):
#         threading.Thread.__init__(self)
#         self._pressed = False
#         self.channel = channel
#         GPIO.setup(self.channel, GPIO.IN)
#         self.deamon = True
#         self.start()

#     def run(self):
#         previous = None
#         while 1:
#             current = GPIO.input(self.channel)
#             time.sleep(0.01)

#             if current is False and previous is True:
#                 self._pressed = True

#                 while self._pressed:
#                     time.sleep(0.05)

#             previous = current

#     def onButtonPress():
#         print("btn presdsed")

# button = Button(36)

# while True:
#     name = input('Enter a Name:')

#     if name.upper() == ('Q'):
#         break
#     print('hello', name)

#     if button.pressed():
#         onButtonPress()



# if __name__ == '__main__':
 
#   logging.basicConfig(level=logging.INFO)
#   # while True:
#   # points = lightMoon(led_coords)
#   # for i in points:
#   #     print (led_coords[i[0]][0], led_coords[i[0]][1])
#     # print (led_coords[point[0][0]])
#     # if last != point:
#     #   last = point
#     # print (led_coords[point[0][0]])
#     # sleep(5)