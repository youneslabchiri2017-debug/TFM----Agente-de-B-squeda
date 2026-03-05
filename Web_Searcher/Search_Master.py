from Web_Searcher.Text_Searchers.General_Searcher import General_Searcher
from Web_Searcher.Text_Searchers.WikiPedia_Searcher import Wikipedia_Searcher

class Search_Master():

    def __init__(self):
        self.wikipedia_searcher = Wikipedia_Searcher()
        self.general_searcher = General_Searcher()

    def search_wikipedia(self, term):
        pass

    def search_urls(self, term):
        pass

