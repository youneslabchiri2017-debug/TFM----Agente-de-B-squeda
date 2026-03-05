import requests

class WikiData_Searcher():

    def __get_knowledge_from_wikidata__(self, term):
        url = "https://query.wikidata.org/sparql"
        query = f"""
            SELECT ?item ?propiedad ?objeto ?propiedadNombre ?objetoNombre WHERE {{
              ?item rdfs:label "{term}"@en .
              ?item ?p ?objeto .

              ?propiedad wikibase:directClaim ?p .
              ?propiedad rdfs:label ?propiedadNombre . 
              FILTER(LANG(?propiedadNombre) = "en")

              ?objeto rdfs:label ?objetoNombre .
              FILTER(LANG(?objetoNombre) = "en")
            }}
            """

        headers = {"Accept": "application/sparql-results+json",
                   "User-Agent":"MySearchBot_1.0"}
        response = requests.get(url, params={'query': query}, headers=headers)

        if response.status_code != 200:
            return None
        else:
            data = []
            for line in response.json()["results"]["bindings"]:
                data.append((term, line["propiedadNombre"]["value"], line["objetoNombre"]["value"]))
            return data

    def search(self, term):
        return self.__get_knowledge_from_wikidata__(term)


res = WikiData_Searcher().search("Oscar Corcho")
print(res)