from nltk.corpus import brown, shakespeare
from nltk.probability import LidstoneProbDist
from nltk.model.ngram import NgramModel

##todo: try shakespeare corpus

NGRAM_MODEL_N = 3
#TRAIN = brown.words(categories='lore') ## just a list of strings
TRAIN = shakespeare.words()
ESTIMATOR = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)

lm = NgramModel(NGRAM_MODEL_N, TRAIN, estimator=ESTIMATOR)
print lm

print lm.generate(40)
print 'done'
