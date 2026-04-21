import requests

class DBpedia_Searcher():

    def __get_knowledge_from_dbpedia__(self, term):
        url = "https://dbpedia.org/sparql"

        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?item ?property ?value ?propertyLabel ?valueLabel WHERE {{
          ?item rdfs:label "{term}"@en .
          ?item ?property ?value .

          OPTIONAL {{
            ?property rdfs:label ?propertyLabel .
            FILTER(LANG(?propertyLabel) = "en")
          }}

          OPTIONAL {{
            ?value rdfs:label ?valueLabel .
            FILTER(LANG(?valueLabel) = "en")
          }}
        }}
        LIMIT 200
        """

        headers = {
            "Accept": "application/sparql-results+json",
            "User-Agent": "MySearchBot_1.0"
        }

        response = requests.get(url, params={"query": query}, headers=headers)

        # 🔍 Debug útil
        if response.status_code != 200:
            print("Error:", response.status_code)
            print(response.text)
            return None

        json_data = response.json()

        if "results" not in json_data:
            print("Respuesta inesperada:", json_data)
            return None

        data = []
        for line in json_data["results"]["bindings"]:
            prop = line.get("propertyLabel", {}).get("value") or line["property"]["value"]
            val = line.get("valueLabel", {}).get("value") or line["value"]["value"]
            data.append((term, prop, val))

        return data

    def search(self, term):
        return self.__get_knowledge_from_dbpedia__(term)