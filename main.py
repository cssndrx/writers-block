import nltk

class Corpus:
    def __init__(self):
        self.text = self.load_brains()

    def load_brains(self):
        with open('teddy.txt', 'r') as f:
            raw = f.read()

        tokens = nltk.wordpunct_tokenize(raw)
        text = nltk.Text(tokens)
        return text

    def word_lookup(self, word):
        return self.text.concordance(word)

    def related_words(self, word):
        return self.text.similar(word)

    def generate(self, context):
        """
        context := list of strings of nearby context upon which to generate
                    e.g ['Mighty', 'fine', 'day', 'we', 'have', 'here']
        """
        return self.text.generate(context=context)
