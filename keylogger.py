#!/usr/bin/python

### TODO: may want to check out cross-platform loggers
### http://stackoverflow.com/questions/365110/cross-platform-keylogger
import pyHook
import win32gui
import win32console

from PyQt4.QtCore import * 
from PyQt4.QtGui import *

LOG_FILE = 'new_log2.txt'


### we need to make decision on what type of inputs get passed to the corpus
### what should happen to punctuation?
### yes, we probably want to treat punctuation as delimiters so that users can get feedback right away.....
def is_searchable(x):
    """
    Returns True if the character should be added to the buffer
    (i.e. if the character might be part of a search string)
    """
    ## TODO: this is probably overly conservative but let's do alphabet-only for now
    return chr(x).isalpha()

def is_delimiter(x):
    """
    Returns True if upon receipt, the word in the buffer should be analyzed
    """
    ## TODO: this also probably needs to be twiddled with...
    ## space or return or punctuation
    ## http://www.asciitable.com/
    return x == 32 or x == 13 or ( x >= 33 and x <= 46) or ( x >= 58 and x <= 64) or (x >= 91 and x <= 96) or (x >= 123 and x <= 126)

def is_dirty_ascii(x):
    """
    Returns True if witnessing the ASCII char will corrupt the buffer
    """
    ## backspace
    return x == 8


class WindowsKeyLogger(QObject):

    def __init__(self, *args):
        QObject.__init__(self, *args)

        ## Holds the best guess of user's last word
        self.buffer = ''

        self.init_logger()

    def init_logger(self):
        ## create hidden window
        window = win32console.GetConsoleWindow()  
        win32gui.ShowWindow(window,0)             

        ## http://sourceforge.net/apps/mediawiki/pyhook/index.php?title=PyHook_Tutorial
        proc = pyHook.HookManager()

        ## register callback to hookmanager
        proc.KeyDown = self.pressed_chars     
        proc.HookKeyboard()              

    def pressed_chars(self, event):
        """
        Process keypress
        """
        ## http://www.asciitable.com/
        print 'buffer before', self.buffer
        if event.Ascii:

            if is_dirty_ascii(event.Ascii):
                self.clear_buffer()

            elif is_searchable(event.Ascii): 
                self.buffer += chr(event.Ascii)

            elif is_delimiter(event.Ascii): 
                ## signal to the text editor that the word is ready
                print 'signal emitted!!', self.buffer

                self.emit(SIGNAL('SPACE_PRESSED')) 
            else:
                print '--'+str(event.Ascii)+'--'
        print 'buffer after', self.buffer
        
    def read_buffer(self):
        return self.buffer

    def clear_buffer(self):
        self.buffer = ''

##    def write_to_log(self, event, log_file=LOG_FILE):
##        """
##        Just for debugging purposes
##        """
##        with open(log_file, 'a') as f:
##            if event.Ascii > 31 and event.Ascii < 127:
##                char = chr(event.Ascii)
##                f.write(char)
##            elif event.Ascii == 13:   ## return
##                f.write('\n')       
##            else:
##                f.write('--'+str(event.Ascii)+'--')


if __name__ == '__main__':
    WindowsKeyLogger()
