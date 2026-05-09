from Project.Specific_Searcher.Category_Searchers.Category_Searcher import Category_Searcher


class Person_Searcher(Category_Searcher):

    def __init__(self):
        Category_Searcher.__init__(self)
        self.attributes_to_search[''] = ""
        self.id_cat = 'Q5'

    def search(self, term):
        super().search(term)
        #Busqueda especifica

    def __search_person__(self):
        pass