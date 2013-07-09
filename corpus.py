import os
import itertools
import nltk
from nltk.util import tokenwrap
from nltk.corpus import wordnet as wn

from nltk_custom import CorpusText
from utils import *
from config import *


def smush(matrix):
    return list(itertools.chain.from_iterable(matrix))
    

#####################################################
#### TODO: put these format funcs somewhere better
def invis(x):
    ## might want to approach whitespace alternatively
    ## http://www.qtcentre.org/threads/27245-Printing-white-spaces-in-QPlainTextEdit-the-QtCreator-way
    return '&nbsp;'*len(x)

def bold(x):
    return '<b>' + x + '</b>'

def identity(x):
    return x

def default_word_format_func(word):
    if word.isalpha() and is_rare_by_threshold(word):
        return bold(word)
    return identity(word)
#####################################################


class CEO(object):
    corpora = []

    def __new__(cls, *args, **kwargs):
        if not cls.corpora:
            cls.load_corpora()
        return super(CEO, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def load_corpora(cls):
        print 'Loading corpora.....'
        for corpus_name, corpus in CORPORA.iteritems():
            print 'Loading.....', corpus_name
            cls.corpora.append(Corpus(corpus_name, corpus))

    @classmethod
    def word_lookup(cls, word):
        ## hit the corpora
        ## get token matrix from each corpus
        results = [corpus.word_lookup(word) for corpus in cls.corpora]

        ## pass the results to the manager(s)
        manager = Manager(10)
        return manager.process_results(results)

    @classmethod
    def get_corpora_names(cls):
        return tokenwrap(str(c) for c in cls.corpora)
  
class Manager(object):

    def __init__(self, num_rows):
        ## maximum number of rows to return
        self.num_rows = num_rows 

    def process_results(self, results):
        ## filter results to get rows sorted by score
        matrix = Manager.filter_results(results, self.num_rows)

        ## choose a formatting function that decorates words
        formatted = Manager.format_matrix(matrix, default_word_format_func)
        
        ## return a string result
        return Manager.matrix_to_str(matrix)

    @staticmethod
    def filter_results(results, num_rows):
        """
        Returns the best num_results of rows as ordered by their self-assigned rankings
        """
        rows = smush( r.matrix for r in results )
        scores = smush( r.get_scores() for r in results )

        zipped = zip(scores, rows)
        zipped.sort(reverse=True)

        ordered_rows = [row for (score, row) in zipped]

        ## return only the best num_results of rows
        if len(ordered_rows) < num_rows:
            return ordered_rows
        return ordered_rows[:num_rows]

    @staticmethod
    def format_matrix(matrix, word_format_func):
        """
        Creates a new matrix with word_format_func applied to each token in a matrix
        """
        tokens = []
        for word_list in matrix:
            row_tokens = []
            dist = get_dist_in_english(word_list)
            for word in word_list:
                row_tokens.append(word_format_func(word))

            tokens.append(row_tokens)
            
        return tokens
    
    @staticmethod
    def matrix_to_str(matrix):
        """
        Creates string repr of the formatted matrix if it DNE
        Returns string repr in all cases
        """

        ##TODO: this might be slow because strings are immutable
        result = ''
        for row in matrix:
            result += tokenwrap(row) + '\n'

        return result
           
    
class Corpus(object):

    def __init__(self, corpus_name, corpus):
        self.corpus_name = corpus_name
        self.text = self.load_corpus(corpus)

        ## dict of previously returned results (word -> Result object)
        ## todo: this will cause memory to grow as the program runs!!! should probably kick some things out
        self.cache = {} 

        ##build indices before the gui renders
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
            raise NotImplemented
        return tokens
    
    def word_lookup(self, word):
        """
        Given a word, return a Result object
        """
        if word in self.cache:
            return self.cache[word]
        
        neighbors = self.text.get_adjacent_tokens(word)
        result = Result(neighbors)
        self.cache[word] = result

        print 'len(result', len(result)
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


class Result(object):
    def __init__(self, matrix):
        self.matrix = matrix if matrix else []

        ## some Nice manager may want to assign these to a Result obj
        self.formatted = [] ## matrix in which tokens have formatting on them e.g. '<b>poppy</b>'
        self.string_repr = '' ## string repr of the formatted matrix

    def get_scores(self):
        """
        Returns the perception of the best rows in the result matrix
        """
        ## todo: actually score the rows
        return [1,] * len(self.matrix)

    def __len__(self):
        return len(self.matrix)
    
##class Library(object):
##    corpora = []
##
##    def __new__(cls, *args, **kwargs):
##        if not cls.corpora:
##            cls.load_corpora()
##        return super(Library, cls).__new__(cls, *args, **kwargs)
##
##    @classmethod
##    def load_corpora(cls):
##        print 'Loading corpora.....'
##        for corpus_name, corpus in CORPORA.iteritems():
##            print 'Loading.....', corpus_name
##            cls.corpora.append(Corpus(corpus_name, corpus))
##    
##    @classmethod
##    def word_lookup(cls, word):
##        return cls.hit_corpora('word_lookup', word)
##    
##    @classmethod
##    def related_words(cls, word):
##        return cls.hit_corpora('related_words', word)
##
##    @classmethod
##    def hit_corpora(cls, corpus_func, word):
##        all_matches = []
##        for corpus in cls.get_health()[:MAX_CORPORA]:
##
##            func = getattr(corpus, corpus_func)
##            result = func(word)
##
####            if corpus_rec:
####                all_matches.append(corpus_rec)
##        
##        return ''.join(x+'\n' for x in all_matches)
##
##
##    @classmethod
##    def get_health(cls):
##        return sorted([corpus for corpus in cls.corpora],
##                          reverse=True,
##                          key = lambda x:x.get_health())
##
##    @classmethod
##    def __str__(cls):
##        return tokenwrap(str(c) for c in cls.corpora)
##
##    @staticmethod
##    def synonyms(word):
##        ## to-do: maybe this should not be in Library
##        results = []
##        for synset in wn.synsets(word):
##            results.extend(synset.lemma_names)
##
##        result_set = set(results)        
##
##        if word in result_set:
##            result_set.remove(word)
##
##        return tokenwrap(result_set)
