from os import system, name
from subprocess import check_call

#Clear the console
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def sysshutdown():
  check_call(['sudo', 'poweroff'])