from Knowledge_Search.Searchers.Searcher import Searcher
import requests

class WikiData_Searcher(Searcher):

    def __init__(self):
        self.requester = requests

    def __get_knowledge_from_wikidata__(self, termino):
        url = "https://query.wikidata.org/sparql"
        query = f"""
            SELECT ?item ?propiedad ?objeto ?propiedadNombre ?objetoNombre WHERE {{
              ?item rdfs:label "{termino}"@es .
              ?item ?p ?objeto .

              ?propiedad wikibase:directClaim ?p .
              ?propiedad rdfs:label ?propiedadNombre . 
              FILTER(LANG(?propiedadNombre) = "es")

              ?objeto rdfs:label ?objetoNombre .
              FILTER(LANG(?objetoNombre) = "es")
            }}
            """

        headers = {"Accept": "application/sparql-results+json"}
        response = self.requester.get(url, params={'query': query}, headers=headers)

        return response.json()["results"]["bindings"]

    def search(self, term):
        return self.__get_knowledge_from_wikidata__(term)