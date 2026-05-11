import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes import neighbors


class Ontology:

    def __init__(self, terms, key_cat, nx = nx):
        if not hasattr(self, "required_properties"):
            self.required_properties = []
        if not hasattr(self, "property_map"):
            self.property_map = {}
        # Same as wikidata
        if not hasattr(self, "rdf_type"):
            self.rdf_type = None
        self.term = terms.term
        self.nx = nx
        #self.validate(terms)
        self.graph = self.build_graph(terms.filtered_data[key_cat], terms.term)

    def build_graph(self, data, term):
        graph = self.nx.Graph()
        #Create graph with normal tuples
        for suj, prop, obj in data[0]:
            if prop in self.property_map:
                graph.add_edge(suj, obj, prop=prop, in_pm=True, is_extra=False)
            else:
                graph.add_edge(suj, obj, prop=prop, in_pm=False, is_extra=False)
        #Complete graph with the extra tuples
        neighbors = list(graph.neighbors(term))
        for suj, prop, obj in data[1]:
            for neighborg in neighbors:
                if suj in neighborg:
                    graph.add_edge(neighborg, obj, prop=prop, in_pm=False, is_extra=True)
                if obj in neighborg:
                    graph.add_edge(neighborg, suj, prop=prop, in_pm=False, is_extra=True)
        return graph

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