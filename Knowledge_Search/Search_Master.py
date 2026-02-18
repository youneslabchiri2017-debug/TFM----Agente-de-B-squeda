from Knowledge_Search.Searchers.Knowledge_Searchers.WikiData_Searcher import WikiData_Searcher
from Knowledge_Search.Searchers.Text_Searchers.General_Searcher import General_Searcher
from Knowledge_Search.Searchers.Text_Searchers.WikiPedia_Searcher import Wikipedia_Searcher


class Search_Master():

    def __init__(self):
        self.wikidata_searcher = WikiData_Searcher()
        self.wikipedia_searcher = Wikipedia_Searcher()
        self.general_searcher = General_Searcher()
        self.knowledge = {}

    def __search_knowledge__(self, term):
        self.knowledge['wikidata'] = self.wikidata_searcher.search(term)
        self.knowledge['wikipedia'] = self.wikipedia_searcher.search(term)
        self.knowledge['general'] = self.general_searcher.search(term)