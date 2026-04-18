from ddgs import DDGS
from Project.Specific_Searcher.Utils.DBpedia_Searcher import DBpedia_Searcher
from Project.Specific_Searcher.Utils.WikiData_Searcher import WikiData_Searcher
from Project.Specific_Searcher.Utils.WikiPedia_Searcher import Wikipedia_Searcher


class Category_Searcher():

    def __init__(self):
        self.wiki_searcher = WikiData_Searcher()
        self.dbpedia_searcher = DBpedia_Searcher()
        self.wikipedia_searcher = Wikipedia_Searcher()
        self.attributes_to_search = {}

    def __search_pages__(self, term, max_res=5):
        with DDGS() as ddgs:
            results = ddgs.text(term, max_results=max_res)
        return list(map(lambda x: x['href'], results))

    def search(self, term):
        term.data['wikidata'] = self.wiki_searcher.search(term.term)
        term.data['dbpedia'] = self.dbpedia_searcher.search(term.term)
        term.data['wikipedia'] = self.wikipedia_searcher.search(term.term)
        print()

