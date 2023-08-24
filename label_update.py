import networkx as nx


class LabelUpdate:
    def retrieve_new_label(self, node, graph, clustering: dict, page_rank: dict, additional_data: dict):
        node_neighbors = additional_data[node]['neighbours']
        neighbors_score = dict()
        for neighbor in node_neighbors:
            neighbor_neighbors = set(additional_data[neighbor]['neighbours'])
            mutual_neighbors = neighbor_neighbors & set(node_neighbors)
            neighbors_score[neighbor] = len(mutual_neighbors)
        neighbors_with_maximum_score = self.find_dictionary_maximum_key(dictionary=neighbors_score)
        if len(neighbors_with_maximum_score) > 1:
            if self.check_maximum_values_are_zero(neighbors_with_maximum_score, neighbors_score):
                new_scores = dict()
                for neighbor in neighbors_with_maximum_score:
                    new_scores[neighbor] = page_rank[neighbor] ** (clustering[neighbor] + 1)
                neighbors_with_maximum_new_score = self.find_dictionary_maximum_key(new_scores)
                return graph.get_node_current_label(neighbors_with_maximum_new_score[0])
            else:
                max_degree_neighbor = (None, 0)
                for neighbor in neighbors_with_maximum_score:
                    neighbor_degree = additional_data[neighbor]['degree']
                    if neighbor_degree > max_degree_neighbor[1]:
                        max_degree_neighbor = (neighbor, neighbor_degree)
                return graph.get_node_current_label(max_degree_neighbor[0])
        else:
            return graph.get_node_current_label(neighbors_with_maximum_score[0])

    def check_maximum_values_are_zero(self, neighbors_with_maximum_score: list, neighbors_score: dict) -> bool:
        for neighbor in neighbors_with_maximum_score:
            if neighbors_score[neighbor] != 0:
                return False
        return True

    def find_dictionary_maximum_key(self, dictionary: dict) -> list:
        max_value = max(dictionary.values())
        return [key for key, value in dictionary.items() if value == max_value]
