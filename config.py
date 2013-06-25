import nltk

CORPUSES = {'Teddy': 'teddy.txt',
            'Emma': nltk.corpus.gutenberg.words('austen-emma.txt')}

#### add all of brown
##for category in nltk.corpus.brown.categories():
##    corpus_name = category.capitalize()
##    corpus = nltk.corpus.brown.sents(categories=category)
##    CORPUSES[corpus_name] = corpus
