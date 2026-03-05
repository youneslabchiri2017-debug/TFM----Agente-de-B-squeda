from Specific_Searcher.Category_Searchers.Taxon_Searcher import Taxon_Searcher
from Specific_Searcher.Category_Searchers.Person_Searcher import Person_Searcher
from Specific_Searcher.Category_Searchers.Place_Searcher import Place_Searcher


class SearchMaster():

    def __init__(self):
        self.person_searcher = Person_Searcher()
        self.place_searcher = Place_Searcher()
        self.taxon_searcher = Taxon_Searcher()

    def search_by_category(self, term):
        if len(term.term_categories) > 0:
            for category in term.term_categories:
                if category == 'Q5':
                    self.person_searcher.search(term)
                elif category == 'Q515' or category == 'Q6256':
                    self.place_searcher.search(term)
                elif category == 'Q16521':
                    self.taxon_searcher.search(term)