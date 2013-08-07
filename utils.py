from config import *
import itertools
import random
import os
import time
from nltk.util import tokenwrap


def is_keylogger():
    """
    Returns True if we are keylogging in order to offer suggestions (Windows-only)
    """
    return os.name == 'nt' and IS_KEYLOGGER

#####################################################
#### general 
#####################################################
def smush(matrix):
    return list(itertools.chain.from_iterable(matrix))

def wrap(iterable):
    return tokenwrap(iterable)

def safe_wrap(iterable):
    ## preserves white space
    return ''.join(x + ' ' for x in iterable)

def get_files_in_directory(directory, ext_filter='', full_path=False):
    files = os.listdir(directory)

    ## filter by extension
    filtered = [f for f in files if f.endswith(ext_filter)] if ext_filter else full_files

    ## return full_path or not
    return [os.path.join(directory, x) for x in filtered] if full_path else filtered
    
def get_corpora():
    corpora = CORPORA.copy()

    def filename_to_prettyname(filename):
        root = filename.split('.')[0]
        return root.capitalize()

    if IS_USING_USER_CORPORA:
        for corpus_name in get_files_in_directory(USER_FOLDER, '.txt'):
            pretty_name = filename_to_prettyname(corpus_name)
            corpora[pretty_name] = corpus_name
    return corpora

def get_datetime_as_str():
    return time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())

def get_date_as_str():
    return time.strftime('%Y-%m-%d', time.localtime())

#####################################################
#### nltk 
#####################################################

##def get_dist_in_english(word_list):
##    occurences = [(w, ENGLISH_DIST[w.lower()]) for w in word_list]
##    return dict(occurences)

def english_freq_count(word):
    return ENGLISH_DIST[word]

def is_rare_by_threshold(word, threshold=3):
    return english_freq_count(word) < threshold

def is_stopword(word):
    return word in STOP_WORDS

    
#####################################################
#### formatting 
#####################################################

def invis(x):
    ## might want to approach whitespace alternatively
    ## http://www.qtcentre.org/threads/27245-Printing-white-spaces-in-QPlainTextEdit-the-QtCreator-way
    return '&nbsp;'*len(x)

def bold(x):
    return '<b>' + x + '</b>'

def identity(x):
    return x

def color(x, color):
    return '<a style="color:%s">' % color + x + '</a>'

def bold_rare_words(word):
    if word.isalpha() and is_rare_by_threshold(word):
        return bold(word)
    return identity(word)

def single_color_rare_words(word, crayon_color='blue'):
    if word.isalpha() and is_rare_by_threshold(word):
        return color(word, crayon_color)
    return identity(word)


def word_to_rgb_str(word):
    """
    Given a word, returns a color
    ## rare ones should be sparkly
    ## boring words should be drab
    """

    def get_low_value():
        return random.randrange(30, 70)

    def get_mid_value():
        return random.randrange(120, 150)

    def get_high_value():
        return random.randrange(170, 210)

    def get_sparkly_rgb():
        indices = range(3)
        random.shuffle(indices)
        values = [get_low_value(), get_mid_value(), get_high_value()]
        zipped = zip(indices, values)
        zipped.sort()
        return [val for ind, val in zipped]

    def get_drab_rgb():
        return [get_low_value() for i in range(3)]

    def rgb_to_str(rgb):
        return 'rgb(%d, %d, %d)' % tuple(rgb)
    
    rgb = get_sparkly_rgb() if is_rare_by_threshold(word) else get_drab_rgb()
    return rgb_to_str(rgb)


def color_map_rare_words(word):
    if word.isalpha():
        crayon_color = word_to_rgb_str(word)
        return color(word, crayon_color)
    return identity(word)


#####################################################
