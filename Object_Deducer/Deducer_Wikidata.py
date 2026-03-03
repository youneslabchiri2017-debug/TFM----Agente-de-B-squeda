import requests
from Object_Deducer.Deducer import Deducer

class Deducer_Wikidata(Deducer):

    def __init__(self):
        super().__init__()
        self.url_wikidata = "https://www.wikidata.org/w/api.php"
        self.super_wiki_url = "https://www.wikidata.org/wiki/Special:EntityData/{}.json"
        self.headers = {
            'User-Agent': 'MiBot'
        }

    def __search_wikidata_objects__(self, term):
        params = {
            "action": "wbsearchentities",
            "language": "en",
            "format": "json",
            "search": term
        }
        data = requests.get(self.url_wikidata, headers=self.headers, params=params).json()

        if data['search']:
            return data['search']
        return None

    def __get_superclasses__(self, qid):
        """Devuelve las superclases directas (P279) y las instancias (P31)."""
        data = requests.get(self.super_wiki_url.format(qid), headers={'User-Agent': 'MiBot'}).json()
        supers = []

        if data['entities']:
            entity = data["entities"][qid]
            claims = entity.get("claims", {})

            # Instancia de (P31)
            if "P31" in claims:
                for claim in claims["P31"]:
                    try:
                        supers.append(claim["mainsnak"]["datavalue"]["value"]["id"])
                    except Exception:
                        pass


            # Subclase de (P279)
            if "P279" in claims:
                for claim in claims["P279"]:
                    try:
                        supers.append(claim["mainsnak"]["datavalue"]["value"]["id"])
                    except Exception:
                        pass

        return supers


    def __get_claims__(self, id):
        params = {
            "action": "wbgetentities",
            "language": "en",
            "format": "json",
            "props": "claims",
            "ids": id
        }
        claims = requests.get(self.url_wikidata, headers=self.headers, params=params).json()
        return claims['entities'][id]['claims']

    def __is_in_set__(self, qid, visited = None):
        if visited == None:
            visited = set()

        if qid in self.ROOT_CLASSES:
            return qid

        if qid in visited:
            return None

        visited.add(qid)

        to_visit = []

        for super_class in self.__get_superclasses__(qid):
            if super_class in self.ROOT_CLASSES:
                return super_class
            to_visit.append(super_class)
        for to_v in to_visit:
            return self.__is_in_set__(to_v, visited)


    def __deduce_type_wikidata__(self, object_id):
        claims = self.__get_claims__(object_id)
        if 'P31' in claims and claims['P31'][0]['mainsnak']['datavalue']['value']['id'] in self.ROOT_CLASSES:
            return (claims['P31'][0]['mainsnak']['datavalue']['value']['id'])
        elif 'P279' in claims and claims['P279'][0]['mainsnak']['datavalue']['value']['id'] in self.ROOT_CLASSES:
            return (self.ROOT_CLASSES[id], id)
        else:
            return self.__is_in_set__(object_id)


    def deduce_object(self, term):
        entities = self.__search_wikidata_objects__(term)
        results = []
        for entitie in entities:
            id = entitie['id']
            d_id = self.__deduce_type_wikidata__(id)
            if d_id and d_id in self.ROOT_CLASSES:
                entitie['in_set'] = d_id
                results.append(entitie)
        return results

ded = Deducer_Wikidata()
results = ded.deduce_object('nintendo')
for res in results:
    print(f"{res['id']} - {ded.ROOT_CLASSES[res['in_set']]}")