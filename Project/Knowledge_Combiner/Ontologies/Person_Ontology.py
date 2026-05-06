from Project.Knowledge_Combiner.Ontologies.Ontology import Ontology

class Person_Ontology(Ontology):

    def __init__(self, terms, nx = None):
        self.required_properties = ['name']
        self.property_map = {
            "name": "schema:name",
            "birthDate": "schema:birthDate",
            "occupation": "schema:occupation",
            "nationality": "schema:nationality"
        }
        if nx:
            super().__init__(terms, nx)
        else:
            super().__init__(terms)
        print("Funciona?")

