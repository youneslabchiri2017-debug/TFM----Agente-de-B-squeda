import requests

def get_knowledge_from_wikidata(termino):
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
    response = requests.get(url, params={'query': query}, headers=headers)

    return response.json()["results"]["bindings"]


termino = "miel"
print(f"Buscando {termino}...")

knowledge_wiki = get_knowledge_from_wikidata(termino)
