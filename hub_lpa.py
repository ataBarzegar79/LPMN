import graph
import merge_phase
from graph import Graph


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
        # nodes_betweenness = nx.betweenness_centrality(self.graph.graph)
        nodes_importance = dict()
        for node in nodes:
            # node_betweenness = nodes_betweenness[node]
            node_neighbours = self.graph.get_node_neighbours(node=node)

            # METHOD 1
            # node_degree = self.graph.get_node_degree(node)
            # neighbor_amounts = 0
            # for neighbour in node_neighbours:
            #     neighbor_amounts += self.graph.get_node_degree(node=neighbour)
            # nodes_importance[node] = node_degree / neighbor_amounts  # finding hub power of each node

            ###  METHOD 2 :RDC
            rdc = 0
            for neighbour in node_neighbours:
                rdc += 1 / self.graph.get_node_degree(node=neighbour)
            nodes_importance[node] = rdc  # finding hub power of each node
        return sorted(nodes_importance.items(), key=lambda x: x[1], reverse=True)

    def get_new_label_of_node(self, node: int) -> int:
        node_neighbors = self.graph.get_node_neighbours(node=node)
        label_count = dict()
        # for neighbor in node_neighbors:
        #     label = self.graph.get_node_current_label(node=neighbor)
        #     if label not in label_count:
        #         label_count[label] = 1
        #     else:
        #         label_count[label] += 1
        # max_value = max(label_count.values())
        # labels_with_max_value = [label for label, count in label_count.items() if count == max_value]
        # if len(labels_with_max_value) > 1:
        return self.get_most_appreciate_label(node_neighbors)
        # else:
        #     return labels_with_max_value[0]

    def get_most_appreciate_label(self, node_neighbors) -> int:
        neighbors_score = dict()
        for neighbor in node_neighbors:
            neighbor_neighbors = set(self.graph.get_node_neighbours(neighbor))
            mutual_neighbors = neighbor_neighbors & set(node_neighbors)
            neighbors_score[neighbor] = len(mutual_neighbors)
        max_value = max(neighbors_score.values())
        neighbors_with_maximum_score = [key for key, value in neighbors_score.items() if value == max_value]
        if len(neighbors_with_maximum_score) > 1:
            max_degree_neighbor = (None, 0)
            for neighbor in neighbors_with_maximum_score:
                neighbor_degree = self.graph.get_node_degree(neighbor)
                if neighbor_degree > max_degree_neighbor[1]:
                    max_degree_neighbor = (neighbor, neighbor_degree)
            return self.graph.get_node_current_label(max_degree_neighbor[0])
        else:
            return self.graph.get_node_current_label(neighbors_with_maximum_score[0])
