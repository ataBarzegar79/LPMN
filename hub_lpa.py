import time

import networkx as nx
import graph
import merge_phase
from graph import Graph
from prioroty import Priority
from label_update import LabelUpdate


class HubLpa:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.nodes = self.graph.get_nodes()

    def perform_algorithm(self):
        nodes_additional_data = dict()
        for node in self.nodes:
            node_degree = self.graph.get_node_degree(node=node)
            node_neighbours = self.graph.get_node_neighbours(node=node)
            nodes_additional_data[node] = {
                'degree': node_degree,
                'neighbours': node_neighbours
            }
            self.graph.set_label_to_node(label=node, node=node)
        nodes_based_on_importance = self.get_important_nodes(nodes_additional_data)
        clustering = nx.clustering(self.graph.graph)
        page_rank = nx.pagerank(self.graph.graph)
        counter = 0
        while True:
            LABELS_BEFORE = [self.graph.get_node_current_label(node) for node in self.nodes]
            counter += 1
            for node in nodes_based_on_importance:
                new_label = self.get_new_label_of_node(node[0], clustering, page_rank, nodes_additional_data)
                self.graph.set_label_to_node(new_label, node[0])
            LABELS_AFTER = [self.graph.get_node_current_label(node) for node in self.nodes]
            if LABELS_BEFORE == LABELS_AFTER:
                break
            if counter > 10:
                break
        merge_start = time.time()
        merge_phase.merge_algorithm(self.graph, nodes_additional_data, page_rank)
        print('merge finished at : ', time.time() - merge_start)
        return counter

    def get_important_nodes(self, nodes_additional_data: dict):
        priority = Priority()
        return priority.give_nodes_priority(self.nodes, nodes_additional_data)

    def get_new_label_of_node(self, node: int, clustering: dict, page_rank: dict, nodes_additional_data: dict) -> int:
        label_update = LabelUpdate()
        return label_update.retrieve_new_label(node, self.graph, clustering, page_rank, nodes_additional_data)
