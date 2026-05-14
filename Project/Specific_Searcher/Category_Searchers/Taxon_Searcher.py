import requests
from Project.Specific_Searcher.Category_Searchers.Category_Searcher import Category_Searcher

class Taxon_Searcher(Category_Searcher):

    def __init__(self):
        Category_Searcher.__init__(self)
        self.attributes_to_search[''] = ""
        self.id_cat = 'Q16521'
        self.base_url = "https://api.gbif.org/v1/species/match"
        self.search_url = "https://api.gbif.org/v1/species/search"

    def search(self, term):
        super().search(term)

    def __search_by_common_species_name__(self, name):


        # Parámetros de la búsqueda
        parametros = {
            "q": name,  # El nombre a buscar
            "qField": "VERNACULAR",  # Le decimos que busque específicamente en nombres comunes
            "limit": 1  # Solo queremos el resultado más relevante (el primero)
        }

        # 2. Hacer la petición GET
        respuesta = requests.get(self.search_url, params=parametros)

        if respuesta.status_code != 200:
            print(f"Error al conectar con GBIF: {respuesta.status_code}")
            return []

        datos = respuesta.json()

        # 3. Comprobar si hay resultados en la lista
        # Como es una búsqueda general, devuelve una lista bajo la clave "results"
        if not datos.get("results"):
            print(f"No se encontró información para el nombre común: '{name}'.")
            return []

        # Nos quedamos con el primer resultado (el match más probable)
        especie_info = datos["results"][0]

        # 4. Transformar los datos a formato de tripleta
        tripletas = []

        # Usamos el nombre científico oficial devuelto por GBIF como Sujeto de la tripleta
        sujeto = especie_info.get("scientificName", "Desconocido")

        info = list(filter(lambda x: not ("key" in x[0].lower()), especie_info.items()))

        for predicado, objeto in info:
            # Filtramos para quedarnos con valores simples (ignorando listas/diccionarios anidados)
            if isinstance(objeto, (str, int, float, bool)):
                predicado_limpio = f"has_{predicado}"
                tripletas.append((name, predicado_limpio, objeto))

        return tripletas

    def special_search(self, term):
        species = list(filter(lambda x: x[1] == "taxon known by this common name", term.data[self.id_cat]['wikidata']))
        data = []
        if not species or len(species) == 0:
            data = self.__search_by_common_species_name__(term.term)
        else:
            for specie in species:
                info = self.__search_taxon__(specie)
                if info:
                    data += info
        return data

    def __search_taxon__(self, name):
        # Configuramos los parámetros de la consulta
        params = {
            "name": name,
            "strict": False,
            "verbose": False
        }

        try:
            # Hacemos la petición GET directamente a la API oficial de GBIF
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()  # Lanza error si la web falla

            data = response.json()

            # Verificamos si hay resultados
            if data.get('matchType') == 'NONE':
                print(f"Aviso: No se encontraron coincidencias para '{name}'")
                return []



            return data

        except Exception as e:
            print(f"Error al conectar con GBIF: {e}")
            return []