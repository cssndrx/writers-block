
This is a Python-based text editor that suggests words as you type based on existing corpora

Cassandra Xia
xiac@mit.edu

=================
 REQUIREMENTS 
=================
- Python 2.7
- PyQt4
- nltk
- nltk's gutenberg and brown corpora, to get these corpora:
>>> import nltk
>>> nltk.download()

If you are running Windows and wish to generate suggestions even when not using the editor, 
additional packages for hooking into global keyboard events are required:
- pywin32
- pyHook

=================
 TO RUN
=================
To select which corpora you use, edit them in config.py. 
Your choice of corpora will strongly affect your results.
If the editor is being slow, try using fewer corpora. 

To run:
python gui.py
