import os
import re
import nltk
from nltk.corpus import wordnet as wn

from nltk_custom import CorpusText
from config import CORPORA_FOLDER, USER_FOLDER
from utils import *
import time
           
    
class Corpus(object):

    def __init__(self, corpus_name, corpus):
        self.corpus_name = corpus_name

        t1 = time.time()
        self.text = self.load_corpus(corpus)
        t2 = time.time()
        time_taken = (t2-t1)*1000.0
        print 'Took %0.3f ms to load corpus %s' % (time_taken, self.corpus_name)


        ## dict of previously returned results (word -> MatrixResult object)
        ## todo: this will cause memory to grow as the program runs!!! should probably kick some things out
        self.cache = {} 

        ## build indices before the gui renders
        ## (without this, you will notice a large lag after the user enters the first word)
        t1 = time.time()

        self.text.concordance('blah')
        self.text.similar('blah')
        self.text.generate() #context=[], length=100)
        wn.synsets('blah')

        t2 = time.time()
        time_taken = (t2-t1)*1000.0
        print 'Took %0.3f ms to build indices for corpus %s' % (time_taken, self.corpus_name)

    def load_corpus(self, corpus): 
        tokens = self.corpus_to_tokens(corpus)
        return CorpusText(tokens)

    def corpus_to_tokens(self, corpus):
        if isinstance(corpus, str):
            try:
                with open(os.path.join(CORPORA_FOLDER, corpus), 'r') as f:
                    raw = f.read()
                    tokens = nltk.wordpunct_tokenize(raw)
            except:
                ## gah this is a total hack
                with open(os.path.join(USER_FOLDER, corpus), 'r') as f:
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
        
#        neighbors = self.text.get_adjacent_tokens(word)
        neighbors = self.text.concordance(word)
        print 'neighbors', neighbors

        result = MatrixResult(neighbors)
        self.cache[word] = result

        return result

    def get_health(self):
        return 1
        
    def related_words(self, word):
        return self.text.similar(word)

    def generate(self, cntxt, lngth):
        """
        context := list of strings of nearby context upon which to generate
                    e.g ['Mighty', 'fine', 'day', 'we', 'have', 'here']
        """
        return self.text.generate(context=cntxt, length=lngth)

    def sandwich(self, word_b, word_a='a'):
        result_set = set(re.findall(word_a + r' \w+ ' + word_b, wrap(self.text)))
        return wrap(r + '\n' for r in result_set)

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
    
