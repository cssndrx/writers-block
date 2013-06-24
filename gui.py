import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from corpus import Corpus, UserHistory
import nltk

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
        font = QFont()
        font.setFamily('Courier')

        lbl1 = QLabel("Write here")
        self.input = MyTextEdit()
        self.input.setFont(font)

        lbl2 = QLabel("Suggestions")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(font)

        lbl3 = QLabel('Corpuses being used')
        self.corpuses = QLineEdit()
        self.corpuses.setReadOnly(True)
        self.corpuses.setFont(font)
        self.corpuses.setText(str(Corpus()))

        # window parameters
        self.setGeometry(100, 100, 800, 700)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(lbl1)
        layout.addWidget(self.input)
        layout.addWidget(lbl2)
        layout.addWidget(self.output)
        layout.addWidget(lbl3)
        layout.addWidget(self.corpuses)
        self.setLayout(layout)

        # connections
        self.connect(self.input, SIGNAL("spacePressed"),
                     self.update)

    def update(self):
        last_word = self.get_last_word()
        if not last_word: return


        UserHistory.add_to_history(last_word,
                                   self.is_hit(last_word))
        print 'health', UserHistory.get_health()

        print 'last_word', last_word
        corpus_output = Corpus.word_lookup(last_word)
        if corpus_output:
            self.output.setText(corpus_output)

    def is_hit(self, word):
        return word in self.output.toPlainText()

    def get_last_word(self):
        tokens = nltk.wordpunct_tokenize(self.input.toPlainText())
        words = [str(t) for t in tokens if str(t).isalpha()]
        print 'words', words

        last_word = words[-1] if len(words) > 0 else None
        return last_word

####################################################################
class MyTextEdit(QTextEdit):
    def __init__(self, *args):
        QTextEdit.__init__(self, *args)
        
    def event(self, event):
        if (event.type()==QEvent.KeyPress) and (event.key()==Qt.Key_Space):
            self.emit(SIGNAL("spacePressed")) 

        return QTextEdit.event(self, event)

####################################################################
if __name__ == "__main__": 
    main()
