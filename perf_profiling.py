import cProfile
import gui

PROFILE_LOG = 'profile_results'
NUM_LINES = 20


## registration of the gui
## loading of the corpora
#cProfile.run('gui.main()', PROFILE_LOG)


import pstats
p = pstats.Stats(PROFILE_LOG)
p.sort_stats('tottime').print_stats(NUM_LINES)


## todo: figure out which of the widgets is slowest
