import os
import nltk
from nltk.util import tokenwrap
from nltk.corpus import wordnet as wn

from nltk_custom import CorpusText
from utils import *
from config import *

MAX_ROWS_DISPLAYED = 15

class CEO(object):
    corpora = [] 
    corpora_health = []
    last_word = ''

    def __new__(cls, *args, **kwargs):
        """
        Uses class variable so that corpora are only read in once
        """
        if not cls.corpora:
            cls.load_corpora()
            cls.corpora_health = [0]*len(cls.corpora)
        return super(CEO, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def load_corpora(cls):
        """
        One-time load of the corpora specified in the config file.
        """
        print 'Loading corpora.....'
        for corpus_name, corpus in CORPORA.iteritems():
            print 'Loading.....', corpus_name
            cls.corpora.append(Corpus(corpus_name, corpus))

    @classmethod
    def get_corpora_names(cls):
        return [c.corpus_name for c in cls.corpora]

    @classmethod
    def get_corpora_health(cls):
        """
        Return a list of (health, corpus_name) tuples sorted with highest health first
        """
        zipped = zip(cls.get_corpora_names(), cls.corpora_health)
        zipped.sort(reverse=True, key=lambda x:x[1])
        return zipped

    @classmethod
    def word_lookup(cls, word):
        """
        Gives word to corpora. Each corpus generates a result matrix.
        Gives result matrices to manager.... which generates a string
        """
        ## hit the corpora
        ## get token matrix from each corpus
        results = [corpus.word_lookup(word) for corpus in cls.corpora]

        ## pass the results to the manager
        ## todo: create more managers
        manager = Manager(MAX_ROWS_DISPLAYED)
        string_repr = manager.process_results(results)

        ## update the last_word that was looked up
        cls.last_word = word
        return string_repr

    @classmethod
    def update_corpora_health(cls, word):
        """
        Given the user's new word, queries against each corpus' last returned matrix
        to see if it had offered the suggestion.

        Increments cls.corpora_health with the number of occurences
        """
        ## todo: can we generate a meaningful percentage?
        if not cls.last_word:
            return

        def count_occurences(word, matrix):
            return sum(row.count(word) for row in matrix)
    
        results = [corpus.word_lookup(cls.last_word) for corpus in cls.corpora]
        counts = [count_occurences(word, r.matrix) for r in results]

        ## todo: this is weighted towards large corpora. we should scale this by runtime of the corpora.
        for i, count in enumerate(counts):
            cls.corpora_health[i] += count

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
        return Manager.matrix_to_str(formatted)

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
            result += tokenwrap(row) + '<br>'

        return result
           
    
class Corpus(object):

    def __init__(self, corpus_name, corpus):
        self.corpus_name = corpus_name
        self.text = self.load_corpus(corpus)

        ## dict of previously returned results (word -> Result object)
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
    
    def word_lookup(self, word):
        """
        Given a word, return a Result object
        """
        if word in self.cache:
            return self.cache[word]
        
        neighbors = self.text.get_adjacent_tokens(word)
        result = Result(neighbors)
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


class Result(object):
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
    
##class Library(object):
##    
##    @classmethod
##    def related_words(cls, word):
##        return cls.hit_corpora('related_words', word)
##
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
##        ## todo: maybe this should not be in Library
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
