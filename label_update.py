import networkx as nx


class LabelUpdate:
    def retrieve_new_label(self, node, graph, clustering: dict, page_rank: dict):
        return self.method_two(graph, node,clustering,page_rank)
        # return self.method_one(graph, node)

    def method_one(self, graph, node):
        node_neighbors = graph.get_node_neighbours(node=node)
        label_count = dict()
        for neighbor in node_neighbors:
            label = graph.get_node_current_label(node=neighbor)
            if label not in label_count:
                label_count[label] = 1
            else:
                label_count[label] += 1
        max_value = max(label_count.values())
        labels_with_max_value = [label for label, count in label_count.items() if count == max_value]
        if len(labels_with_max_value) > 1:
            return self.method_two(graph, node)
        else:
            return labels_with_max_value[0]

    def method_two(self, graph, node, clustering: dict, page_rank: dict) -> int:
        node_neighbors = graph.get_node_neighbours(node=node)
        neighbors_score = dict()
        for neighbor in node_neighbors:
            neighbor_neighbors = set(graph.get_node_neighbours(neighbor))
            mutual_neighbors = neighbor_neighbors & set(node_neighbors)
            neighbors_score[neighbor] = len(mutual_neighbors)
        max_value = max(neighbors_score.values())
        neighbors_with_maximum_score = [key for key, value in neighbors_score.items() if value == max_value]
        if len(neighbors_with_maximum_score) > 1:
            if self.check_maximum_values_are_zero(neighbors_with_maximum_score, neighbors_score):
                new_scores = dict()
                # sum = 0
                for neighbor in neighbors_with_maximum_score:
                    # for second_neighbor in graph.get_node_neighbours(neighbor):
                    #     sum += clustering[second_neighbor]
                    new_scores[neighbor] = page_rank[neighbor] ** (clustering[neighbor] + 1)
                max_score = max(new_scores.values())
                neighbors_with_maximum_score = [key for key, value in new_scores.items() if value == max_score]
                return graph.get_node_current_label(neighbors_with_maximum_score[0])
            else:
                max_degree_neighbor = (None, 0)
                for neighbor in neighbors_with_maximum_score:
                    neighbor_degree = graph.get_node_degree(neighbor)
                    if neighbor_degree > max_degree_neighbor[1]:
                        max_degree_neighbor = (neighbor, neighbor_degree)
                return graph.get_node_current_label(max_degree_neighbor[0])
        else:
            return graph.get_node_current_label(neighbors_with_maximum_score[0])

    def check_maximum_values_are_zero(self, neighbors_with_maximum_score: list, neighbors_score: dict) -> bool:
        for key in neighbors_with_maximum_score:
            if neighbors_score[key] != 0:
                return False
        return True
