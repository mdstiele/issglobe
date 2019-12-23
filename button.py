from threading import Timer
import select
import sys
from gpiozero import Button #GPIOzero

#-----------------------------------------#
# use case:
# code starts when pi turns on
# press button will cycle mode
# hold button for 5 seconds shuts down pi
#-----------------------------------------#

# colors change?

def checkButton(timeout):
  #wait for button press till timeout
  #return action
  #0 = nothing
  #1 = modechange
  #2 = shutdown

  button = Button(14)
  while True:
    if button.is_pressed:
      print("Pressed")

class TimeoutExpired(Exception):
    pass

def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [],[], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n') # expect stdin to be line-buffered
    raise TimeoutExpired

def chkChangeMode(timer, currMode):
  try:
    answer = input_with_timeout("Mode:", timer)
  except TimeoutExpired:
    print("Cycle Complete: Mode staying at %d" % int(currMode))
    return currMode
  else:
    if (int(answer) >= 0) and (int(answer) <= 3):
      currMode = answer
    print('Mode updated to %s' % int(currMode))
    return currMode

# def changeModeTwo(currMode)
#   modeList = [1,2,3,0]
#   currMode = modeList[currMode]