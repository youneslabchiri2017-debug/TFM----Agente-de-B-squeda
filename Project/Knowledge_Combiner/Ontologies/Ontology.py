import networkx as nx
import matplotlib.pyplot as plt
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from DB_Access.DB_Controller import DB_Controller
from urllib.parse import quote


class Ontology:

    def __init__(self, terms, key_cat, db = DB_Controller(), nx = nx):
        if not hasattr(self, "required_properties"):
            self.required_properties = []
        if not hasattr(self, "property_map"):
            self.property_map = {}
        # Same as wikidata
        if not hasattr(self, "rdf_type"):
            self.rdf_type = None
        self.db = db
        self.term = terms.term
        self.nx = nx
        self.SCHEMA = Namespace("http://schema.org/")
        self.LOCAL = Namespace("http://tu_proyecto.org/resource/")
        self.EXTRA = Namespace("http://tu_proyecto.org/properties/extra/")
        self.url = "http://localhost:7200/repositories/KnowledgeDB"
        self.graph = self.build_graph(terms.filtered_data[key_cat], terms.term)

    def clean_for_uri(self, text):
        """
        Convierte cualquier texto en una cadena 100% segura para ser usada como URI.
        Reemplaza espacios por guiones bajos y codifica símbolos raros.
        """
        # 1. Convertimos a string y cambiamos espacios por guiones bajos
        texto_str = str(text).replace(" ", "_")
        # 2. quote codifica las comillas, paréntesis, tildes, etc.
        # El parámetro safe="_-" asegura que no nos modifique los guiones
        return quote(texto_str, safe="_-")

    def build_graph(self, data, term):
        main_subject = self.LOCAL[term.replace(" ", "_")]
        rdf_g = Graph()
        type_url = self.rdf_type.replace("schema:", str(self.SCHEMA))
        rdf_g.add((main_subject, RDF.type, URIRef(type_url)))
        for u, attr, v in data[0]:
            sujeto = self.LOCAL[self.clean_for_uri(u)]
            #if self.db.term_exists(term):
            objeto = self.LOCAL[self.clean_for_uri(v)]
            if attr in self.property_map:
                clean_prop = attr.replace("schema:", "").replace(" ", "_")
            else:
                clean_prop = attr.replace(" ", "_")
            pred_uri = self.SCHEMA[clean_prop]

            rdf_g.add((sujeto, pred_uri, objeto))
        for u, attr, v in data[1]:
            sujeto = self.LOCAL[self.clean_for_uri(u)]
            # if self.db.term_exists(term):
            objeto = self.LOCAL[self.clean_for_uri(v)]
            if attr in self.property_map:
                clean_prop = attr.replace("schema:", "").replace(" ", "_")
            else:
                clean_prop = attr.replace(" ", "_")
            pred_uri = self.EXTRA[clean_prop]

            rdf_g.add((sujeto, pred_uri, objeto))
        return rdf_g



    def validate(self, data):
        return all(prop in data for prop in self.required_properties)

    def draw_graph(self):
        G = self.graph
        pos = nx.spring_layout(G)

        # 4. Dibujar el grafo
        plt.figure(figsize=(8, 6))
        nx.draw(
            G, pos,
            with_labels=True,  # Mostrar los nombres de los nodos
            node_color='skyblue',  # Color del nodo
            node_size=2000,  # Tamaño del nodo
            edge_color='gray',  # Color de las líneas
            font_size=12,  # Tamaño de la letra
            font_weight='bold'  # Negrita para las etiquetas
        )

        # 5. Mostrar con Matplotlib
        plt.title("Visualización de Grafo con NetworkX")
        plt.show()

    def draw_limited_graph(self, center, N=20):
        # Obtener vecinos directos del nodo central
        neighbors = list(self.graph.neighbors(center))

        # Limitar a los primeros N vecinos
        limited_neighbors = neighbors[:N]

        # Crear lista de nodos a incluir (centro + vecinos)
        nodes_to_include = [center] + limited_neighbors

        # Crear subgrafo
        subgraph = self.graph.subgraph(nodes_to_include)

        # Layout
        pos = nx.spring_layout(subgraph, seed=42)

        # Colores de aristas según in_pm
        edge_colors = [
            "red" if d.get("in_pm") else "gray"
            for _, _, d in subgraph.edges(data=True)
        ]

        # Dibujar nodos
        nx.draw_networkx_nodes(subgraph, pos, node_color="lightblue", node_size=800)

        # Dibujar etiquetas
        nx.draw_networkx_labels(subgraph, pos, font_size=8)

        # Dibujar aristas
        nx.draw_networkx_edges(subgraph, pos, edge_color=edge_colors, width=2)

        # Etiquetas de aristas
        edge_labels = nx.get_edge_attributes(subgraph, "prop")
        nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, font_size=6)

        plt.axis("off")
        plt.show()