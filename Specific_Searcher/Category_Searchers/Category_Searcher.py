from ddgs import DDGS
from Specific_Searcher.Utils.WikiData_Searcher import WikiData_Searcher

class Category_Searcher():

    def __init__(self):
        self.wiki_searcher = WikiData_Searcher()
        self.attributes_to_search = {}

    def __search_pages__(self, term, max_res=5):
        with DDGS() as ddgs:
            results = ddgs.text(term, max_results=max_res)
        return list(map(lambda x: x['href'], results))

    def search(self, term):
        term.term_categories = self.wiki_searcher.search(term.term)