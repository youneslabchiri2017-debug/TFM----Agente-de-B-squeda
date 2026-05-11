from Project.Knowledge_Combiner.Ontologies.Country_Ontology import Country_Ontology
from Project.Knowledge_Combiner.Ontologies.Person_Ontology import Person_Ontology
from Project.Knowledge_Combiner.Ontologies.Taxon_Ontology import Taxon_Ontology
from DB_Access.DB_Controller import DB_Controller


class Ontology_Master:

    def __init__(self):
        self.ontologys = {
            "Q5": Person_Ontology,
            "Q16521": Taxon_Ontology,
            "Q6256": Country_Ontology
        }
        self.db_acces = DB_Controller()

    # Se tiene que crear un nuevo grafo a partir del objeto "Termino"
    def create_graph(self, terms, save_g = True):
        # Persona
        for key_id in terms.filtered_data:
            cat = key_id.split('-')[0]
            if cat in self.ontologys:
                ontology = self.ontologys[cat](terms, key_id)
                #ontology.draw_limited_graph(terms.term)
                #ontology.draw_graph()
                terms.ontologyes[key_id] = ontology
        print(f"Tenemos {len(terms.ontologyes)} ontologias listas")
        if save_g:
            self.db_acces.save_knowledge(terms.ontologyes)


    # Combina lo que ya existe con los nuevos datos recolectados
    def combine_knowledge(self, new_knowledge, old_knowledge):
        return new_knowledge

    # Guarda los grafos nuevos o conocimiento ya existente
    def save_knowledge(self, graph_knowledge):
        pass

    # Regresa lo que hay en la base de datos sobre este termino
    def load_knowledge(self, term):
        return None