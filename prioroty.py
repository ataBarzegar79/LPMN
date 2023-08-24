from graph import Graph


class Priority:
    def give_nodes_priority(self, nodes, nodes_additional_data: dict) -> list:
        nodes_importance = dict()
        for node in nodes:
            node_neighbours = nodes_additional_data[node]['neighbours']
            node_degree = nodes_additional_data[node]['degree']
            neighbor_amounts = 0
            for neighbour in node_neighbours:
                neighbor_amounts += nodes_additional_data[neighbour]['degree']
            nodes_importance[node] = node_degree / neighbor_amounts
        return sorted(nodes_importance.items(), key=lambda x: x[1], reverse=True)
