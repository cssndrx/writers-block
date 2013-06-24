import nltk

DEFAULT_CORPUS = 'teddy.txt'
DEFAULT_CORPUS = nltk.corpus.gutenberg.words('austen-emma.txt')

class Corpus(object):
    _instance = None
    text = ''

    def __new__(cls, *args, **kwargs):
        if not cls.text:
            cls.text = cls.load_corpus()
        return super(Corpus, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def load_corpus(cls):
        print 'Loading corpus.....'
        corpus = DEFAULT_CORPUS

        if isinstance(corpus, str):
            with open(corpus, 'r') as f:
                raw = f.read()
                tokens = nltk.wordpunct_tokenize(raw)
        elif isinstance(corpus, nltk.corpus.reader.util.StreamBackedCorpusView):
            tokens = corpus

        text = nltk.Text(tokens)
        return text

    @classmethod
    def word_lookup(cls, word):
        return cls.text.concordance(word)

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
        return 'working??'

