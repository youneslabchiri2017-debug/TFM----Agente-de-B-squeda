import networkx as nx

class Ontology:

    def __init__(self, terms, nx = nx):
        self.required_properties = []
        self.property_map = {}
        self.nx = nx
        #self.validate(terms)
        self.graph = self.build_graph(terms.filtered_data)

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