import nltk

DEFAULT_CORPUS = nltk.corpus.gutenberg.words('austen-emma.txt')
DEFAULT_CORPUS = 'teddy.txt'

class Corpus(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Corpus, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self, corpus=DEFAULT_CORPUS):
        self.corpus = corpus
        self.text = self.load_corpus(corpus)

    def load_corpus(self, corpus):
        print 'Loading corpus.....'

        if isinstance(corpus, str):
            with open(corpus, 'r') as f:
                raw = f.read()
                tokens = nltk.wordpunct_tokenize(raw)
        elif isinstance(corpus, nltk.corpus.reader.util.StreamBackedCorpusView):
            tokens = corpus

        text = nltk.Text(tokens)
        return text

    def word_lookup(self, word):
        return self.text.concordance(word)

    def related_words(self, word):
        return self.text.similar(word)

    def generate(self, context=[]):
        """
        context := list of strings of nearby context upon which to generate
                    e.g ['Mighty', 'fine', 'day', 'we', 'have', 'here']
        """
        return self.text.generate(context=context)

    def __str__(self):
        return str(self.corpus)

if __name__ == '__main__':
    s1=Corpus()
    s2=Corpus()
    if(id(s1)==id(s2)):
        print "Same"
    else:
        print "Different"
        assert False, 'singularity violated'

    print 'return', s1.word_lookup("the")
    print 'return', s1.related_words("the")
    print 'return', s1.generate("the")
