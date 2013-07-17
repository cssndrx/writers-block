# Natural Language Toolkit: Texts
#
# Copyright (C) 2001-2012 NLTK Project
# Author: Steven Bird <sb@csse.unimelb.edu.au>
#         Edward Loper <edloper@gradient.cis.upenn.edu>
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT

"""
This module brings together a variety of NLTK functionality for
text analysis, and provides simple, interactive interfaces.
Functionality includes: concordancing, collocation discovery,
regular expression search over tokenized strings, and
distributional similarity.
"""

from nltk.probability import FreqDist, LidstoneProbDist
from nltk.util import tokenwrap
from nltk.model import NgramModel

##from math import log
##from collections import defaultdict
##import re
##
##from nltk.probability import ConditionalFreqDist as CFD
##from nltk.util import tokenwrap, LazyConcatenation
##from nltk.metrics import f_measure, BigramAssocMeasures
##from nltk.collocations import BigramCollocationFinder

import nltk

class StaticGoodness(object):
    """
    Object to judge the "goodness" or interesting-ness of text.
    Not inherited from nltk. todo: perhaps this should be moved elsewhere like Corpus
    """
    def __init__(self, text):
        pass

    def get_goodness(self):

        ## frequency distribution on words

        ## humans determine goodness by comparing against a reference

        ## different goodness depending on what you are doing
        ## creative writing:
        ## technical writing:

        ## unusualness and ability to make you think

        ## disorder constrained by 


        ## the easiest heuristic is just to do it based on length
        pass
    
class CorpusText(nltk.Text):
    def concordance(self, word, width=79, lines=25):
        """
        Return a string concordance for ``word`` with the specified context window.
        Word matching is not case-sensitive.
        :seealso: ``ConcordanceIndex``

        (nltk default is to print concordance)
        """
        if '_concordance_index' not in self.__dict__:
            print "Building concordance index..."
            self._concordance_index = CorpusConcordanceIndex(self.tokens,
                                                       key=lambda s:s.lower())

        return self._concordance_index.get_concordance_as_str(word, width, lines)

    def similar(self, word, num=20):
        """
        Returns as a string similar words
        """
        if '_word_context_index' not in self.__dict__:
            print 'Building word-context index...'
            self._word_context_index = nltk.ContextIndex(self.tokens,
                                                    filter=lambda x:x.isalpha(),
                                                    key=lambda s:s.lower())

#        words = self._word_context_index.similar_words(word, num)

        word = word.lower()
        wci = self._word_context_index._word_to_contexts
        if word in wci.conditions():
            contexts = set(wci[word])
            fd = FreqDist(w for w in wci.conditions() for c in wci[w]
                          if c in contexts and not w == word)
            words = fd.keys()[:num]
            return tokenwrap(words)
        else:
            print "No matches"

    def generate(self, length=100, context=()):
        """
        Return random text, generated using a trigram language model.

        :param length: The length of text to generate (default=100)
        :type length: int
        :seealso: NgramModel
        """
        if '_trigram_model' not in self.__dict__:
            print "Building ngram index..."
            estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
            self._trigram_model = NgramModel(3, self, estimator=estimator)
        text = self._trigram_model.generate(length, context=context)
        return tokenwrap(text)


    def get_adjacent_tokens(self, word, window=5, lines=25):
        ### todo: should this go here??? look into fixing nltk.ContentIndex
## to-do: figure out what to do about capitalization        
##        assert word == word.lower()

        result = []        

        indices = [ i for i, w in enumerate(self.tokens) if w.lower()==word]
        if indices:
            lines = min(lines, len(indices))
            print "Displaying %s of %s matches:" % (lines, len(indices))

            for i in indices:
                if lines <= 0:
                    break

                ind_a = max(0, i-window)
                ind_b = min(len(self.tokens), i+window)
                
                adjacent = self.tokens[ind_a:ind_b]
                result.append(adjacent)
                lines -= 1
        else:
            print "No matches"

        return result

class CorpusConcordanceIndex(nltk.ConcordanceIndex):
            
##    def print_concordance(self, word, width=75, lines=25):
##        """
##        Print a concordance for ``word`` with the specified context window.
##
##        :param word: The target word
##        :type word: str
##        :param width: The width of each line, in characters (default=80)
##        :type width: int
##        :param lines: The number of lines to display (default=25)
##        :type lines: int
##        """
##        half_width = (width - len(word) - 2) / 2
##        context = width/4 # approx number of words of context
##
##        offsets = self.offsets(word)
##        if offsets:
##            lines = min(lines, len(offsets))
##            print "Displaying %s of %s matches:" % (lines, len(offsets))
##            for i in offsets:
##                if lines <= 0:
##                    break
##                left = (' ' * half_width +
##                        ' '.join(self._tokens[i-context:i]))
##                right = ' '.join(self._tokens[i+1:i+context])
##                left = left[-half_width:]
##                right = right[:half_width]
##                print left, self._tokens[i], right
##                lines -= 1
##        else:
##            print "No matches"
            
    def get_concordance_as_str(self, word, width=75, lines=25):
        """
        Returns a string of the concordance.
        Returns None if no matches found

        (nltk default is to print concordance)
        """
        concordance_str = ""

        half_width = (width - len(word) - 2) / 2
        context = width/4 # approx number of words of context

        offsets = self.offsets(word)
        if offsets:
            lines = min(lines, len(offsets))
            print "Displaying %s of %s matches:" % (lines, len(offsets))
            for i in offsets:
                if lines <= 0:
                    break
                left = (' ' * half_width +
                        ' '.join(self._tokens[i-context:i]))
                right = ' '.join(self._tokens[i+1:i+context])
                left = left[-half_width:]
                right = right[:half_width]
                concordance_str += left + ' ' + self._tokens[i] + ' ' + right + '\n'
                lines -= 1
            return concordance_str
        else:
            print "No matches"
