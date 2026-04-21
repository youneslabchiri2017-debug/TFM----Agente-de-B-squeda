from Project.Knowledge_Combiner.Ontologies.Person_Ontology import Person_Ontology

class Ontology_Master:

    def __init__(self):
        self.ontologys = {
            "Q5": Person_Ontology
        }

    # Se tiene que crear un nuevo grafo a partir del objeto "Termino"
    def create_graph(self, terms):
        # Persona
        for category in terms.term_categories:
            if category in self.ontologys:
                ontology = self.ontologys[category](terms)

    # Combina lo que ya existe con los nuevos datos recolectados
    def combine_knowledge(self, new_knowledge, old_knowledge):
        return new_knowledge

    # Guarda los grafos nuevos o conocimiento ya existente
    def save_knowledge(self, graph_knowledge):
        pass

    # Regresa lo que hay en la base de datos sobre este termino
    def load_knowledge(self, term):
        return None