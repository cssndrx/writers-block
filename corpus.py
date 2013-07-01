import os
import nltk
import itertools
from config import CORPORA, CORPORA_FOLDER

MAX_CORPORA = min(len(CORPORA), 3)

def get_english_words(word_list):
    text_vocab = set(w.lower() for w in word_list if w.isalpha())
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    return list(text_vocab.intersection(english_vocab))

def sort_by_unusual(word_list):
    ## make sure that it is a word
    english_words = get_english_words(word_list)
    print 'english_words', english_words

    ## pick the word that has the lowest freq distribution in the english language
    fdist = nltk.FreqDist([w.lower() for w in nltk.corpus.words.words()])
    return english_words.sort(key = lambda x: fdist[x])

def format_by_unusual(raw):
    if not raw:
        return raw

    print 'raw', raw
    tokens = nltk.wordpunct_tokenize(raw)
    tokens = sort_by_unusual(tokens)

    if not tokens:
        return
    
    weirdest = tokens[0]

    ind = raw.find(weirdest)
    formatted = raw[:ind] + '<b>' + weirdest + '</b>' + raw[ind:]
    print 'weirdest', weirdest
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
        all_matches = []
        for corpus in cls.get_health()[:MAX_CORPORA]:
            corpus_rec = corpus.word_lookup(word)
            if corpus_rec:
                all_matches.append(corpus_rec)
        
        return ''.join([x+'\n' for x in all_matches])

##    ## todo: remove this code duplication with word_lookup
##    @classmethod
##    def related_words(cls, word):
##        all_matches = []
##        for corpus in cls.get_health()[:MAX_CORPORA]:
##            corpus_rec = corpus.related_words(word)
##            if corpus_rec:
##                all_matches.append(corpus_rec)
##        
##        return ''.join([x+'\n' for x in all_matches])

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
        print 'hit corpus init'
        self.text.concordance('blah')
        
    def load_corpus(self, corpus):
        tokens = self.corpus_to_tokens(corpus)
        return nltk.Text(tokens)

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
        
        rec = self.text.concordance(word)

        ##should remove this
#        rec = "".join(x+' ' for x in rec)

#        rec = format_by_unusual(rec)
        if rec:
            self.last_rec = rec
            self.health.append(word) ## +health for having it in the corpus
        else:
            self.health.append(None)
        return rec        

    def get_health(self):
        return 1 - self.health.count(None) / float(len(self.health) + 1)
    
    def __str__(self):
        return self.corpus_name
    
    def related_words(self, word):
        return self.text.similar(word)

    def generate(self, context=[]):
        """
        context := list of strings of nearby context upon which to generate
                    e.g ['Mighty', 'fine', 'day', 'we', 'have', 'here']
        """
        return self.text.generate(context=context)


