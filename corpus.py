import nltk
import itertools
from config import CORPUSES
        

class Corpus(object):
    texts = {}
    active = []

    def __new__(cls, *args, **kwargs):
        if not cls.texts:
            cls.load_corpus()
        return super(Corpus, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def load_corpus(cls):
        print 'Loading corpuses.....'
        for corpus_name, corpus in CORPUSES.iteritems():

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

            text = nltk.Text(tokens)

            ## eck... corpus is not immutable and should not be uesd as a key
            cls.texts[corpus_name] = text
            cls.active.append(corpus_name)

    @classmethod
    def word_lookup(cls, word):
        result = ''
        for corpus_name in cls.active:
            concordance = cls.texts[corpus_name].concordance(word)
            if concordance:
                result += concordance + '\n'
        return result

    @classmethod
    def related_words(cls, word):
        return cls.text.similar(word)

    @classmethod
    def generate(cls, context=[]):
        """
        context := list of strings of nearby context upon which to generate
                    e.g ['Mighty', 'fine', 'day', 'we', 'have', 'here']
        """
        return cls.text.generate(context=context)

    @classmethod
    def __str__(cls):
        return ''.join([x+' ' for x in CORPUSES.keys()])


class UserHistory(object):

    ## keeps track of user history
    ## number of suggestions that were taken, etc.

    user_history = []
    hit_or_miss = []

    @classmethod
    def add_to_history(cls, word, isHit):
        cls.user_history.append(word)
        cls.hit_or_miss.append(isHit)

    @classmethod
    def get_health(cls):
        return sum(cls.hit_or_miss)/float(len(cls.hit_or_miss))
