import nltk

CORPUSES = {'Teddy': 'teddy.txt',
            'Emma': nltk.corpus.gutenberg.words('austen-emma.txt'),
            'Romance': nltk.corpus.brown.sents(categories='romance')}
