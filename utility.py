import sys
import select
import tty
import subprocess
import termios

def clearScreen():
    subprocess.call('clear', shell=True)

def keyPressed(key):
    if key in ('W', 'w'):
        return 0
    elif key in ('A', 'a'):
        return 1
    elif key in ('D', 'd'):
        return 2
    elif key in ('E', 'e'):
        return 3
    elif key in ('S', 's'):
        return 4


class NonBlockingInput():
    """
    Utility Class
    -> Clearing Screen
    -> Non-Blocking Inputs (NBIs)
    """
    def __init__(self):
        self.oldSettings = termios.tcgetattr(sys.stdin)
    
    @classmethod
    def NBISetupTerminal(cls):
        '''
        Sets up the terminal for non-blocking input
        '''
        tty.setcbreak(sys.stdin.fileno())

    def originalTerminal(self):
        '''
        Sets terminal back to original state
        '''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.oldSettings)

    @classmethod
    def isKeyPressed(cls):
        '''
        returns True if keypress has occured
        '''
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    @classmethod
    def getCharecter(cls):
        '''
        returns input character
        '''
        return sys.stdin.read(1)

    @classmethod
    def flush(cls):
        '''
        clears input buffer
        '''
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    
