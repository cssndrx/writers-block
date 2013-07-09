import os
import sys
import time
import nltk
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

from corpus import CEO
from config import CORPORA, IS_KEYLOGGER

## todo: figure out where this should go
font = QFont('Courier', 12, QFont.Light)

def main():
    app = QApplication(sys.argv) 
    w = MyWindow() 
    w.show()

    sys.exit(app.exec_()) 

def is_keylogger():
    return os.name == 'nt' and IS_KEYLOGGER
    

def input_box():
    """
    Returns an input box that raises a QT SIGNAL
    in response to the space bar
    """
    inp = SpacebarTextEdit()
    inp.setFont(font)
    return inp

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

def output_grid():
    pass

def vstack_widgets(widgets, with_stretch=False):
    """
    Returns a layout that vertically stacks the given widgets
    """
    layout = QVBoxLayout()
    for i, w in enumerate(widgets):
        layout.addWidget(w)

        if with_stretch and i%2==1:
            ## assumes that widgets are paired when adding stretches
            layout.addStretch(1)

    return layout

        
class MyWindow(QWidget): 

    def __init__(self, *args):
        
        QWidget.__init__(self, *args)

        ## attributes
        self.input = input_box()
        self.output = output_box()
        self.words = output_line()
        self.update_time = output_word()
        self.last_word = output_word()
        self.corpora_health = output_grid()


        ## load the CEO for interacting with corpora
        ceo = CEO()

        # create window
        self.setGeometry(40, 40, 1000, 800)
        self.build_window()

        ## make connections to register signals
        self.register_events()
        
    def build_window(self):
        # build sublayouts
        wide_widgets = [lbl('Write here'),
                        self.input,
                        lbl('Suggestions'),
                        self.output,
                        lbl('Word suggestions'),
                        self.words,
                        ]
        self.wide_layout = vstack_widgets(wide_widgets)

        narrow_widgets = [lbl('Update time'),
                          self.update_time,
                          lbl('Last_word'),
                          self.last_word,
                          lbl('Corpora being used'),
                          self.corpora_health,
                          ]
        self.narrow_layout = vstack_widgets(narrow_widgets, with_stretch=True)

        ## build main layout
        layout = QHBoxLayout()
        layout.addLayout(self.wide_layout)
        layout.addLayout(self.narrow_layout)
        self.setLayout(layout)
        
    def register_events(self):
        """
        Registers QT signal so that 'update' function is called after the user enters a word
        """
        if is_keylogger(): 
            from keylogger import WindowsKeyLogger
            self.sniffer = WindowsKeyLogger()
            self.connect(self.sniffer, SIGNAL('SPACE_PRESSED'),
                         self.update)
        else:
            self.connect(self.input, SIGNAL('SPACE_PRESSED'),
                         self.update)
        
    def update(self):
        """
        Called after user finishes typing a word
        """
        t1 = time.time()

        last_word = self.get_last_word()
        if not last_word: return
        self.last_word.setText(last_word)

        corpus_output = CEO.word_lookup(last_word)
        if corpus_output: self.output.setHtml(corpus_output)
       
        t2 = time.time()
        time_taken = (t2-t1)*1000.0
        self.update_time.setText('%0.3f ms' % time_taken)

            
    def get_last_word(self):
        """
        Identifies the last word from either the Windows keylogger or the GUI element
        """
        if is_keylogger():
            last_word = self.sniffer.read_buffer()
            self.sniffer.clear_buffer()
        else:
            tokens = nltk.wordpunct_tokenize(self.input.toPlainText())
            words = [str(t) for t in tokens if str(t).isalpha()]
            last_word = words[-1] if len(words) > 0 else None

        return last_word
        

class SpacebarTextEdit(QTextEdit):
    """
    An input box that raises a QT SIGNAL
    in response to the space bar
    """
    def __init__(self, *args):
        QTextEdit.__init__(self, *args)
        
    def event(self, event):
        if (event.type()==QEvent.KeyPress) and (event.key()==Qt.Key_Space):
            self.emit(SIGNAL('SPACE_PRESSED')) 

        return QTextEdit.event(self, event)


if __name__ == "__main__": 
    main()

######## RELATED WORDS STUFF #########
#### this is backwards looking.... so it doesn't work very well 
###        related_words = Library.related_words(last_word)
##        related_words = Library.synonyms(last_word)
##        if related_words: self.words.setText(related_words)


######## CHUCK WIDGET STUFF #########
##        if not hasattr(self, 'test_widget'):
##            self.test_widget = QLabel('BOOM')
##            self.narrow_layout.addWidget(self.test_widget)
##        else:
##            self.test_widget.hide()

###### HEALTH STUFF #########
##        # track the health
##        healthGrid = QGridLayout()
##
##        self.healthLabel = []
##        for i, corpus_name in enumerate(CORPORA.keys()):
##            self.healthLabel.append( (QLabel(corpus_name), QLabel('-')) )
##            healthGrid.addWidget(self.healthLabel[i][0], i, 0)
##            healthGrid.addWidget(self.healthLabel[i][1], i, 1)


##    def render_health(self):        
##        for i, c in enumerate(Library.get_health()):
##            self.healthLabel[i][0].setText(c.corpus_name)
##            self.healthLabel[i][1].setText('%.2f' % c.get_health())
