from Project.Filters.Knowledge_Filter import Knowledge_Filter
from Project.Knowledge_Combiner.Ontology_Master import Ontology_Master
from Project.Specific_Searcher.Category_Searchers.Taxon_Searcher import Taxon_Searcher
from Project.Specific_Searcher.Category_Searchers.Person_Searcher import Person_Searcher
from Project.Specific_Searcher.Category_Searchers.Place_Searcher import Place_Searcher


class SearchMaster():

    def __init__(self):
        # Searchers
        self.person_searcher = Person_Searcher()
        self.place_searcher = Place_Searcher()
        self.taxon_searcher = Taxon_Searcher()
        # Filters
        self.filter = Knowledge_Filter()
        self.knowledge_m = Ontology_Master()

    def search_by_category(self, term):
        if len(term.term_categories) > 0:
            for category in term.term_categories:
                try:
                    if category == 'Q5':
                        self.person_searcher.search(term)
                    elif category == 'Q515' or category == 'Q6256':
                        self.place_searcher.search(term)
                    elif category == 'Q16521':
                        self.taxon_searcher.search(term)
                except Exception as e:
                    print(e)
            self.filter.filter(term)
            old_graph = self.knowledge_m.load_knowledge(term)
            # El termino ya existe
            if old_graph:
                new_graph = self.knowledge_m.create_graph(term)
                self.knowledge_m.combine_knowledge(new_graph, old_graph)
                self.knowledge_m.save_knowledge(new_graph)
            # El termino no existe
            else:
                new_graph = self.knowledge_m.create_graph(term)
                self.knowledge_m.save_knowledge(new_graph)
