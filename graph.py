from typing import Set, Any

import networkx as nx
import matplotlib.pyplot as plt


# noinspection PyMethodMayBeStatic
# as we are using networkx package
# graph class is just a wrapper !
class Graph:

    def __init__(self, graph_file_path):
        self.graph = None
        self.graph_file_path = graph_file_path
        self.read_graph_from_path()
        self.colors = ['#C0C0C0', '#FF0000', '#800080', '#00FF00', '#faebd7',
                       '#d2691e', '#00ffff', '#bdb76b', '#9932cc', '#ff1493',
                       '#ffd700', '#ff69b4', '#4b0082', '#7cfc00', '#ffa07a',
                       '#000080', '#ffa500', '#00ff7f', '#9acd32', '#f5f5f5',
                       '#cacfd2', '#7b7d7d', '#909497', '#9b59b6', '#c0392b',
                       '#d4efdf', '#616a6b', '#cacfd2', '#7b7d7d', '#909497',
                       '#9b59b6', '#5499c7', '#2471a3', '#5b2c6f', '#117a65',
                       '#a93226', '#d4efdf', '#85c1e9', '#5499c7', '#2471a3',
                       '#5b2c6f', '#117a65', '#a93226',
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

    def get_labels(self) -> set[Any]:
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
