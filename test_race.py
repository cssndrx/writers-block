from keylogger import WindowsKeyLogger
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
import sys


sniffer = WindowsKeyLogger()


class MainWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.connect(sniffer, SIGNAL('SPACE_PRESSED'),
                         self.update)

    def update(self):
        print 'hit here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        ## do something really slow
        
        
app = QApplication(sys.argv) 

w = MainWindow() 
w.show()
sys.exit(app.exec_()) 
