from Project.Specific_Searcher.Category_Searchers.Category_Searcher import Category_Searcher


class Place_Searcher(Category_Searcher):

    def __init__(self):
        Category_Searcher.__init__(self)
        self.attributes_to_search[''] = ""
        # For the moment it only search for countrys
        self.id_cat = 'Q6256'

    def search(self, term):
        pass
        #super().search(term)

    def __search_place__(self):
        pass