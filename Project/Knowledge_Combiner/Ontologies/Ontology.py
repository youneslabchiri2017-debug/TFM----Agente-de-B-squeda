import networkx as nx
import matplotlib.pyplot as plt

class Ontology:

    def __init__(self, terms, key_cat, nx = nx):
        if not hasattr(self, "required_properties"):
            self.required_properties = []
        if not hasattr(self, "property_map"):
            self.property_map = {}
        self.nx = nx
        #self.validate(terms)
        self.graph = self.build_graph(terms.filtered_data[key_cat])

    def build_graph(self, data):
        graph = self.nx.Graph()
        for suj, prop, obj in data:
            if prop in self.property_map:
                graph.add_edge(suj, obj, prop=prop, in_pm=True)
            else:
                graph.add_edge(suj, obj, prop=prop, in_pm=False)
        return graph

    def validate(self, data):
        return all(prop in data for prop in self.required_properties)

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