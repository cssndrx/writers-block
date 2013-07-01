import os
import itertools
import nltk
from nltk.util import tokenwrap

from nltk_custom import CorpusText
from config import CORPORA, CORPORA_FOLDER


MAX_CORPORA = min(len(CORPORA), 3)

ENGLISH_SET = set(w.lower() for w in nltk.corpus.words.words())
ENGLISH_DIST = nltk.FreqDist(nltk.corpus.words.words()) ##HAHA THIS IS WRONG TO-DO

def get_english_words(word_list):
    ## assumes that all words are lower case
    ## incomplete check
    if word_list: assert word_list[0] == word_list[0].lower()
    
    text_vocab = set(word_list)
    return list(text_vocab.intersection(ENGLISH_SET))

def sort_by_unusual(word_list):
    word_list = [w.lower() for w in word_list]

    ## make sure that it is a word
    english_words = get_english_words(word_list)

    ## pick the word that has the lowest freq distribution in the english language
    print 'english_words', [(ENGLISH_DIST[x], x) for x in english_words]
    english_words.sort(key = lambda x: ENGLISH_DIST[x])
    return english_words

def process_matrix(matrix):
    formatted = ""
    for row in matrix:

        tokens = sort_by_unusual(row)

        if not tokens:
            return
        
        weirdest = tokens[0]
        print 'weirdest', weirdest
        ind = [x.lower() for x in row].index(weirdest)

        row[ind] = '<b>' + row[ind] + '</b>'

        formatted += tokenwrap(row) + '\n' ###todo: this string concat might be inefficient?
    return formatted
            

class Library(object):
    corpora = []

    def __new__(cls, *args, **kwargs):
        if not cls.corpora:
            cls.load_corpora()
        return super(Library, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def load_corpora(cls):
        print 'Loading corpora.....'
        for corpus_name, corpus in CORPORA.iteritems():
            print 'Loading.....', corpus_name
            cls.corpora.append(Corpus(corpus_name, corpus))
    
    @classmethod
    def word_lookup(cls, word):
        return cls.hit_corpora('word_lookup', word)
    
    @classmethod
    def related_words(cls, word):
        return cls.hit_corpora('related_words', word)

    @classmethod
    def hit_corpora(cls, corpus_func, word):
        all_matches = []
        for corpus in cls.get_health()[:MAX_CORPORA]:

            func = getattr(corpus, corpus_func)
            corpus_rec = func(word)
            if corpus_rec:
                all_matches.append(corpus_rec)
        
        return ''.join(x+'\n' for x in all_matches)


    @classmethod
    def get_health(cls):
        return sorted([corpus for corpus in cls.corpora],
                          reverse=True,
                          key = lambda x:x.get_health())

    @classmethod
    def __str__(cls):
        return ''.join(str(corpus)+' ' for corpus in cls.corpora)
    
class Corpus(object):

    def __init__(self, corpus_name, corpus):
        self.corpus_name = corpus_name
        self.text = self.load_corpus(corpus)
        self.last_rec = ''
        self.health = []

        ##build indices before the gui renders
        self.text.concordance('blah')
        self.text.similar('blah')
        
    def load_corpus(self, corpus):
        tokens = self.corpus_to_tokens(corpus)
        return CorpusText(tokens)

    def corpus_to_tokens(self, corpus):
        ## this is sketchy.... fix this
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
    
    def update_health(self, word):
        if word.lower() in self.last_rec.lower():
            self.health.append(word) ## +health for having it in the recommendation
        else:
            self.health.append(None)
    
    def word_lookup(self, word):
        self.update_health(word)
        
#        rec = self.text.concordance(word)
#        rec = str(self.text.get_adjacent_tokens(word))

        neighbors = self.text.get_adjacent_tokens(word)
        rec = process_matrix(neighbors)
        
#        rec = format_by_unusual(rec)
        if rec:
            self.last_rec = rec
            self.health.append(word) ## +health for having it in the corpus
        else:
            self.health.append(None)
        return rec        

    def get_health(self):
        return 1 - self.health.count(None) / float(len(self.health) + 1)
        
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
