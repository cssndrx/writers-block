from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize

sent_tokenize('Hello SF Python.  This is NLTK. Mary...')
##word_tokenize('This is NLTK.')
##
##from nltk.tag import pos_tag
##words = word_tokenize('And now for something completely different.')
##pos_tag(words)
##
##from nltk.chunk import ne_chunk
##ne_chunk(pos_tag(word_tokenize('My name is Jacob Perkins.')))
##
###### text classification
####import nltk.data
####classifer = nltk.data.load('classifiers/movie_reviews_NaiveBayes.pickle')
####classifer.classify(['great', 'movie'])
##
##print 'done'
