from Project.Knowledge_Combiner.Ontologies.Ontology import Ontology

class Person_Ontology(Ontology):

    def __init__(self, terms):
        self.required_properties = ['name']
        self.property_map = {
            "name": "schema:name",
            "birthDate": "schema:birthDate",
            "occupation": "schema:occupation",
            "nationality": "schema:nationality"
        }
        super(Person_Ontology, self).__init__(terms)
        print("Funciona?")

