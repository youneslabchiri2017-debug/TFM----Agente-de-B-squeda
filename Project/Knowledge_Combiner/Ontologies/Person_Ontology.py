from Project.Knowledge_Combiner.Ontologies.Ontology import Ontology

class Person_Ontology(Ontology):

    def __init__(self, terms, key_id, nx = None):
        self.required_properties = ['name']
        self.rdf_type = "schema:Person"
        self.property_map = {
            "name": "schema:name",
            "birthDate": "schema:birthDate",
            "occupation": "schema:occupation",
            "nationality": "schema:nationality",
            "sex": "schema:nationality"
        }
        if nx:
            super().__init__(terms, key_id, nx)
        else:
            super().__init__(terms, key_id)

