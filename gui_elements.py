from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

from utils import *


## todo: figure out where this should go
font = QFont('Courier', 12, QFont.Light)

def input_box():
    """
    Returns an input box that raises a QT SIGNAL
    in response to the space bar
    """
    inp = SpacebarTextEdit()
    inp.setFont(font)
    return inp

def btn(init_text='-'):
    return QPushButton(init_text)

def lbl(init_text='-'):
    return QLabel(init_text)

def output_box():
    out = QTextEdit()
    out.setReadOnly(True)
    out.setAcceptRichText(True)
    out.setFont(font)
    return out

def output_line():
    out = QLineEdit()
    out.setReadOnly(True)
    out.setFont(font)
    return out

def output_word():
    return lbl()

def output_grid(entries):
    """
    Takes an iterable of tuple-pairs and returns a grid layout
    """
    grid = QGridLayout()
    for i, (a, b) in enumerate(entries):
        grid.addWidget(a, i, 0)
        grid.addWidget(b, i, 1)
    return grid

def update_grid(grid, entries):
    """
    Takes an iterable of tuple-pairs and updates a grid layout
    """
    for i, (a, b) in enumerate(entries):
        grid.itemAtPosition(i, 0).widget().setText(str(a))
        grid.itemAtPosition(i, 1).widget().setText(str(b))


def vstack_widgets(widgets, with_stretch=False):
    """
    Returns a layout that vertically stacks the given widgets
    """
    layout = QVBoxLayout()
    for i, w in enumerate(widgets):
        if isinstance(w, QWidget):
            layout.addWidget(w)
        elif isinstance(w, QLayout):
            layout.addLayout(w)
        else:
            raise NotImplementedError('Tried to add unknown type %s to layout' % type(w))
            
        if with_stretch and i%2==1:
            ## assumes that widgets are paired when adding stretches
            layout.addStretch(1)

    return layout

def health_widget():
    entries = [ (lbl(corpus_name), lbl()) for corpus_name in get_corpora().keys()]
    return output_grid(entries)

class SpacebarTextEdit(QTextEdit):
    """
    An input box that raises a QT SIGNAL in response to the space bar
    """
    def __init__(self, *args):
        QTextEdit.__init__(self, *args)
        
    def event(self, event):
        if (event.type()==QEvent.KeyPress) and (event.key()==Qt.Key_Space):
            self.emit(SIGNAL('SPACE_PRESSED')) 

        return QTextEdit.event(self, event)
