import os
import nltk
from nltk.corpus import wordnet as wn

from nltk_custom import CorpusText
from config import CORPORA_FOLDER
from utils import *
           
    
class Corpus(object):

    def __init__(self, corpus_name, corpus):
        self.corpus_name = corpus_name
        self.text = self.load_corpus(corpus)

        ## dict of previously returned results (word -> MatrixResult object)
        ## todo: this will cause memory to grow as the program runs!!! should probably kick some things out
        self.cache = {} 

        ## build indices before the gui renders
        ## (without this, you will notice a large lag after the user enters the first word)
        self.text.concordance('blah')
        self.text.similar('blah')
        wn.synsets('blah')
        
    def load_corpus(self, corpus): 
        tokens = self.corpus_to_tokens(corpus)
        return CorpusText(tokens)

    def corpus_to_tokens(self, corpus):
        if isinstance(corpus, str):
            with open(os.path.join(CORPORA_FOLDER, corpus), 'r') as f:
                raw = f.read()
                tokens = nltk.wordpunct_tokenize(raw)
        elif isinstance(corpus, nltk.corpus.reader.util.ConcatenatedCorpusView):
            tokens = list(itertools.chain(*corpus))
        elif isinstance(corpus, nltk.corpus.reader.util.StreamBackedCorpusView):
            tokens = corpus
        else:
            raise NotImplementedError('Unkown corpus received of type %s' % type(corpus))
        return tokens
    
    def grep(self, word):
        """
        Given a word, return a Result object
        """
        if word in self.cache:
            return self.cache[word]
        
        neighbors = self.text.get_adjacent_tokens(word)
        result = MatrixResult(neighbors)
        self.cache[word] = result

        return result

    def get_health(self):
        return 1
        
    def related_words(self, word):
        return self.text.similar(word)

    def generate(self, context=[]):
        """
        context := list of strings of nearby context upon which to generate
                    e.g ['Mighty', 'fine', 'day', 'we', 'have', 'here']
        """
        return self.text.generate(context=context)

    def __str__(self):
        return self.corpus_name


class LineResult(object):
    def __init__(self, line):
        self.line = line if line else []

    def get_scores(self):
        ## todo: actually score this
        return [1, ] * len(self.line)

    def __len__(self):
        return len(self.line)

class MatrixResult(object):
    def __init__(self, matrix):
        self.matrix = matrix if matrix else []

##        ## some Nice manager may want to assign these to a Result obj
##        self.formatted = [] ## matrix in which tokens have formatting on them e.g. '<b>poppy</b>'
##        self.string_repr = '' ## string repr of the formatted matrix

    def get_scores(self):
        """
        Returns the perception of the best rows in the result matrix
        """
        ## todo: actually score the rows
        return [1,] * len(self.matrix)

    def __len__(self):
        return len(self.matrix)
    
