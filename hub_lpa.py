import graph
import merge_phase
from graph import Graph
from prioroty import Priority
from label_update import LabelUpdate



class HubLpa:
    def __init__(self, graph: Graph):
        self.graph = graph

    def perform_algorithm(self):
        nodes = self.graph.get_nodes()
        for node in nodes:  # label initialization  => O(n)
            self.graph.set_label_to_node(label=node, node=node)
        nodes_based_on_importance = self.get_important_nodes(nodes=nodes)  # => O(nk)
        counter = 0
        while True:
            LABELS_BEFORE = [self.graph.get_node_current_label(node) for node in nodes]
            counter += 1
            for node in nodes_based_on_importance:
                new_label = self.get_new_label_of_node(node[0])
                self.graph.set_label_to_node(new_label, node[0])
            LABELS_AFTER = [self.graph.get_node_current_label(node) for node in nodes]
            if LABELS_BEFORE == LABELS_AFTER:
                break
            if counter > 10:
                break
        merge_phase.merge_algorithm(self.graph)
        return counter

    def get_important_nodes(self, nodes):
        priority = Priority()
        return priority.give_nodes_priority(self.graph)

    def get_new_label_of_node(self, node: int) -> int:
        label_update = LabelUpdate()
        return label_update.retrieve_new_label(node, self.graph)
