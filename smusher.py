import nltk

### try to string the text back together
with open('nine_stories.txt', 'r') as f:
    raw = f.read()


tokens = nltk.wordpunct_tokenize(raw)
print tokens[:50]
## for each adjacent pair
## check to see if they can form a new word

words = []
i = 0
while i < len(tokens)-1:
    test_word = tokens[i] + tokens[i+1]
    if test_word in nltk.corpus.words.words() or test_word.lower() in nltk.corpus.words.words():
        words.append(test_word)
        print 'found', test_word
        i += 2
    else:
        words.append(tokens[i])
        i += 1

with open('nine_stories_smush.txt', 'w') as g:
    g.write(str(words))

