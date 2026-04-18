from Project.Specific_Searcher.Category_Searchers.Category_Searcher import Category_Searcher


class Person_Searcher(Category_Searcher):

    def __init__(self):
        super(Person_Searcher, self).__init__()
        self.attributes_to_search[''] = ""

    def search(self, term):
        super().search(term)
        #Busqueda especifica

    def __search_person__(self):
        pass