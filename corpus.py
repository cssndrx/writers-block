import nltk
import itertools
from config import CORPUSES
        
class Library(object):
    corpuses = []

    def __new__(cls, *args, **kwargs):
        if not cls.corpuses:
            cls.load_corpuses()
        return super(Library, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def load_corpuses(cls):
        print 'Loading corpuses.....'
        for corpus_name, corpus in CORPUSES.iteritems():
            print 'Loading.....', corpus_name
            cls.corpuses.append(Corpus(corpus_name, corpus))
    
    @classmethod
    def word_lookup(cls, word):
        result = ''
        for corpus in cls.corpuses:
            word_rec = corpus.word_lookup(word)
            if word_rec:
                result += word_rec + '\n'
        return result

    @classmethod
    def get_health(cls):
        return [(c.corpus_name, c.get_health()) for c in cls.corpuses]

    @classmethod
    def __str__(cls):
        return ''.join(str(corpus)+' ' for corpus in cls.corpuses)
    
class Corpus(object):

    def __init__(self, corpus_name, corpus):
        self.corpus_name = corpus_name
        self.text = self.load_corpus(corpus)
        self.last_rec = ''
        self.health = []
        
    def load_corpus(self, corpus):
        tokens = self.corpus_to_tokens(corpus)
        return nltk.Text(tokens)

    def corpus_to_tokens(self, corpus):
        ## this is sketchy.... fix this
        if isinstance(corpus, str):
            with open(corpus, 'r') as f:
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
            self.health.append(word)
        else:
            self.health.append(None)
    
    def word_lookup(self, word):
        self.update_health(word)
        
        rec = self.text.concordance(word)
        if rec: self.last_rec = rec
        return rec

    def get_health(self):
        return 1 - self.health.count(None) / float(len(self.health))
    
    def __str__(self):
        return self.corpus_name
    
##    @classmethod
##    def related_words(cls, word):
##        return cls.text.similar(word)
##
##    @classmethod
##    def generate(cls, context=[]):
##        """
##        context := list of strings of nearby context upon which to generate
##                    e.g ['Mighty', 'fine', 'day', 'we', 'have', 'here']
##        """
##        return cls.text.generate(context=context)


