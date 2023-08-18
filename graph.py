import networkx as nx
import matplotlib.pyplot as plt


# noinspection PyMethodMayBeStatic
# as we are using networkx package
# graph class is just a wrapper !
class Graph:

    def __init__(self, graph_file_path):
        if isinstance(graph_file_path, str):
            self.graph = None
            self.graph_file_path = graph_file_path
            self.read_graph_from_path()
        else:
            self.graph = graph_file_path
        self.colors = [
            '#C0C0C0', '#FF0000', '#800080', '#00FF00', '#FAEBD7',
            '#D2691E', '#00FFFF', '#BDB76B', '#9932CC', '#FF1493',
            '#FFD700', '#FF69B4', '#4B0082', '#7CFC00', '#FFA07A',
            '#000080', '#FFA500', '#00FF7F', '#9ACD32', '#F5F5F5',
            '#CACFD2', '#7B7D7D', '#909497', '#9B59B6', '#C0392B',
            '#D4EFDF', '#616A6B', '#5499C7', '#2471A3', '#5B2C6F',
            '#117A65', '#A93226', '#85C1E9', '#FFFACD', '#FFE4E1',
            '#FFF0F5', '#FAFAD2', '#FFEFD5', '#FAF0E6', '#FFF5EE',
            '#F8F8FF', '#F0F8FF', '#F5FFFA', '#E6E6FA', '#E0FFFF',
            '#FFF8DC', '#E9967A', '#FFDAB9', '#FA8072', '#FFA07A',
            '#20B2AA', '#6B8E23', '#ADFF2F', '#FFFF00', '#FFE4B5',
            '#8A2BE2', '#9400D3', '#BA55D3', '#00CED1', '#1E90FF',
            '#6495ED', '#8A2BE2', '#7FFF00', '#FF4500', '#FFD700',
            '#2E8B57', '#DC143C', '#00FFFF', '#FF6347', '#FF4500',
            '#8A2BE2', '#2E8B57', '#00FF7F', '#4682B4', '#8B4513',
            '#DAA520', '#8A2BE2', '#00FF7F', '#4682B4', '#8B4513',
            '#DAA520', '#D2691E', '#B8860B', '#32CD32', '#FA8072',
            '#D2691E', '#B8860B', '#32CD32', '#FA8072', '#2E8B57',
            '#6A5ACD', '#4B0082', '#FF4500', '#A52A2A', '#800000',
            '#FF0000', '#8A2BE2', '#9370DB', '#663399', '#800080',
            '#0000FF', '#FF00FF', '#1E90FF', '#008080', '#00CED1',
            '#20B2AA', '#32CD32', '#3CB371', '#2E8B57', '#006400',
            '#556B2F', '#8B4513', '#D2691E', '#8A2BE2', '#9932CC',
            '#9370DB', '#663399', '#4B0082', '#800080', '#FF00FF',
            '#8B008B', '#BA55D3', '#DB7093', '#C71585', '#CD5C5C',
            '#FF6347', '#FF4500', '#FFD700', '#ADFF2F', '#32CD32',
            '#008000', '#006400', '#008080', '#00BFFF', '#1E90FF',
            '#0000FF', '#000080', '#4B0082', '#8A2BE2', '#9400D3',
            '#BA55D3', '#FF00FF', '#FF69B4', '#FF1493', '#C71585',
            '#FF4500', '#FFA500', '#FFFF00', '#ADFF2F', '#00FF00',
            '#32CD32', '#20B2AA', '#00FFFF', '#1E90FF', '#0000FF',
            '#8A2BE2', '#9932CC', '#BA55D3', '#FF00FF', '#FF1493',
            '#9370DB', '#663399', '#4B0082', '#800080', '#FF00FF',
            '#8B008B', '#BA55D3', '#DB7093', '#C71585', '#CD5C5C',
            '#FF6347', '#FF4500', '#FFD700', '#ADFF2F', '#32CD32',
            '#008000', '#006400', '#008080', '#00BFFF', '#1E90FF',
            '#0000FF', '#000080', '#4B0082', '#8A2BE2', '#9400D3',
            '#BA55D3', '#FF00FF', '#FF69B4', '#FF1493', '#C71585',
            '#FF4500', '#FFA500', '#FFFF00', '#ADFF2F', '#00FF00',
            '#32CD32', '#20B2AA', '#00FFFF', '#1E90FF', '#0000FF',
            '#8A2BE2', '#9932CC', '#BA55D3', '#FF00FF', '#FF1493',
            '#9370DB', '#663399', '#4B0082', '#800080', '#FF00FF',
            '#8B008B', '#BA55D3', '#DB7093', '#C71585', '#CD5C5C',
            '#FF6347', '#FF4500', '#FFD700', '#ADFF2F', '#32CD32',
            '#008000', '#006400', '#008080', '#00BFFF', '#1E90FF',
            '#0000FF', '#000080', '#4B0082', '#8A2BE2', '#9400D3',
            '#BA55D3', '#FF00FF', '#FF69B4', '#FF1493', '#C71585',
            '#FF4500', '#FFA500', '#FFFF00', '#ADFF2F', '#00FF00',
            '#32CD32', '#20B2AA', '#00FFFF', '#1E90FF', '#0000FF'
        ]

    def read_graph_from_path(self):
        self.graph = nx.read_gml(self.graph_file_path, label='id')
        return self.graph

    def get_nodes_and_data(self):
        return self.graph.nodes.data()

    def get_nodes(self) -> list:
        """
        :return:
            list[]: items of nodes , each node is int .
        """
        return list(self.graph.nodes)

    def get_node_neighbours(self, node):
        return list(self.graph.adj[node])

    def get_node_degree(self, node: int) -> int:
        return len(self.get_node_neighbours(node=node))

    def set_label_to_node(self, label, node):
        self.graph.nodes.data()[node]['label'] = label

    def get_node_current_label(self, node):
        return self.graph.nodes.data()[node]['label']

    def update_labels_in_graph(self, label, node):
        node_current_label = self.get_node_current_label(node)
        for other_node in self.get_nodes():
            if self.get_node_current_label(other_node) == node_current_label:
                self.set_label_to_node(label, other_node)

    def draw_graph(self):
        colors_reserved = {color: None for color in self.colors}
        for node in self.get_nodes():
            node_label = self.get_node_current_label(node)
            if node_label not in colors_reserved.values():
                colors_reserved = self.set_value_to_color(colors_reserved, node_label)
        node_colors = self.get_labels_as_color(colors_reserved)
        nx.draw_networkx(self.graph, node_color=node_colors)
        plt.show()

    def set_value_to_color(self, colors_reserved: dict, node_label) -> dict:
        for key, value in colors_reserved.items():
            if value is None:
                colors_reserved[key] = node_label
                break
        return colors_reserved

    def get_labels_as_color(self, colors_reserved) -> list:
        colors_as_label = []
        for node in self.get_nodes():
            node_label = self.get_node_current_label(node)
            label_color = list(colors_reserved.keys())[list(colors_reserved.values()).index(node_label)]
            colors_as_label.append(label_color)
        return colors_as_label

    def get_labels(self):
        labels = set()
        for node in self.get_nodes():
            labels.add(self.get_node_current_label(node))
        return labels

    def sort_graph_based_on_degree_centrality(self):
        return nx.degree_centrality(self.graph)

    def calculate_modularity(self):
        communities = dict()
        for node in self.get_nodes():
            node_current_label = self.get_node_current_label(node=node)
            if node_current_label not in communities:
                communities[node_current_label] = {node}
            else:
                communities[node_current_label].add(node)
        return nx.community.modularity(self.graph, [v for v in communities.values()])
