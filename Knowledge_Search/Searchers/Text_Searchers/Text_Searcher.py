from Knowledge_Search.Searchers.Searcher import Searcher
from Knowledge_Search.Transformers.Text_Transformer import Text_Transformer

class TextSearcher(Searcher):

    def __init__(self):
        self.transformer = Text_Transformer()

    def search(self, term):
        pass