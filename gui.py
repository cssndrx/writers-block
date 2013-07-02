import sys
import nltk
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

from corpus import Corpus, Library
from config import CORPORA

#################################################################### 
def main(): 
    app = QApplication(sys.argv) 
    w = MyWindow() 
    w.show() 
    sys.exit(app.exec_()) 

####################################################################
class MyWindow(QWidget): 
    def __init__(self, *args): 
        QWidget.__init__(self, *args)

        # create objects
        font = QFont('Courier', 12, QFont.Light)

        ## todo: remove this code duplication
        lbl1 = QLabel("Write here")
        self.input = MyTextEdit()
        self.input.setFont(font)

        lbl2 = QLabel("Suggestions")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setAcceptRichText(True)
        self.output.setFont(font)

        lbl3 = QLabel('Corpora being used')
        self.corpora = QLineEdit()
        self.corpora.setReadOnly(True)
        self.corpora.setFont(font)
        self.corpora.setText(str(Library()))

        lbl4 = QLabel('Word suggestions')
        self.words = QLineEdit()
        self.words.setReadOnly(True)
        self.words.setFont(font)

        # track the health
        healthGrid = QGridLayout()
        self.healthLabel = []
        for i, corpus_name in enumerate(CORPORA.keys()):
            self.healthLabel.append( (QLabel(corpus_name), QLabel('-')) )
            healthGrid.addWidget(self.healthLabel[i][0], i, 0)
            healthGrid.addWidget(self.healthLabel[i][1], i, 1)


        # window parameters
        self.setGeometry(40, 40, 1000, 800)

        # layout
        text_layout = QVBoxLayout()
        text_layout.addWidget(lbl1)
        text_layout.addWidget(self.input)
        text_layout.addWidget(lbl2)
        text_layout.addWidget(self.output)
        text_layout.addWidget(lbl4)
        text_layout.addWidget(self.words)


        health_layout = QVBoxLayout()
        health_layout.addWidget(lbl3)
        health_layout.addLayout(healthGrid)
        health_layout.addStretch(1)

        layout = QHBoxLayout()
        layout.addLayout(text_layout)
        layout.addLayout(health_layout)

        self.setLayout(layout)

        # connections
        self.connect(self.input, SIGNAL('SPACE_PRESSED'),
                     self.update)

    def update(self):
        last_word = self.get_last_word()
        if not last_word: return

        print 'last_word', last_word
        corpus_output = Library.word_lookup(last_word)
#        if corpus_output: self.output.setText('<html>'+corpus_output+'</html>')
        if corpus_output: self.output.setHtml(corpus_output)
       
## this is backwards looking.... so it doesn't work very well 
#        related_words = Library.related_words(last_word)
        related_words = Library.synonyms(last_word)
        if related_words: self.words.setText(related_words)

        self.render_health()
        
    def get_last_word(self):
        tokens = nltk.wordpunct_tokenize(self.input.toPlainText())
        words = [str(t) for t in tokens if str(t).isalpha()]
        print 'words', words

        last_word = words[-1] if len(words) > 0 else None
        return last_word

    def render_health(self):        
        for i, c in enumerate(Library.get_health()):
            self.healthLabel[i][0].setText(c.corpus_name)
            self.healthLabel[i][1].setText('%.2f' % c.get_health())
        
####################################################################
class MyTextEdit(QTextEdit):
    def __init__(self, *args):
        QTextEdit.__init__(self, *args)
        
    def event(self, event):
        if (event.type()==QEvent.KeyPress) and (event.key()==Qt.Key_Space):
            self.emit(SIGNAL('SPACE_PRESSED')) 

        return QTextEdit.event(self, event)

####################################################################
if __name__ == "__main__": 
    main()
