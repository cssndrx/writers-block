import nltk

CORPORA = {'Teddy': 'teddy.txt',
#            'Engelbart': '1962paper.txt',
            'Emma': nltk.corpus.gutenberg.words('austen-emma.txt'),
           'Romance': nltk.corpus.brown.sents(categories='romance')}

CORPORA_FOLDER = 'data'

#### add all of brown
##for category in nltk.corpus.brown.categories():
##    corpus_name = category.capitalize()
##    corpus = nltk.corpus.brown.sents(categories=category)
##    CORPORA[corpus_name] = corpus
