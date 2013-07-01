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

##from math import log
##from collections import defaultdict
##import re
##
##from nltk.probability import FreqDist, LidstoneProbDist
##from nltk.probability import ConditionalFreqDist as CFD
##from nltk.util import tokenwrap, LazyConcatenation
##from nltk.model import NgramModel
##from nltk.metrics import f_measure, BigramAssocMeasures
##from nltk.collocations import BigramCollocationFinder

import nltk

class CorpusText(nltk.Text):
    def concordance(self, word, width=79, lines=25):
        """
        Return a string concordance for ``word`` with the specified context window.
        Word matching is not case-sensitive.
        :seealso: ``ConcordanceIndex``

        (nltk default is to print concordance)
        """
        if '_concordance_index' not in self.__dict__:
            print "Building index..."
            self._concordance_index = CorpusConcordanceIndex(self.tokens,
                                                       key=lambda s:s.lower())

        return self._concordance_index.get_concordance_as_str(word, width, lines)


class CorpusConcordanceIndex(nltk.ConcordanceIndex):

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
