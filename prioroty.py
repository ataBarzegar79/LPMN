from graph import Graph


class Priority:
    def give_nodes_priority(self, graph: Graph) -> list:
        nodes = graph.get_nodes()
        nodes_importance = self.method_one(nodes, graph)
        return sorted(nodes_importance.items(), key=lambda x: x[1], reverse=True)

    def method_one(self, nodes, graph):  # Ata
        nodes_importance = dict()
        for node in nodes:
            node_neighbours = graph.get_node_neighbours(node=node)
            node_degree = graph.get_node_degree(node)
            neighbor_amounts = 0
            for neighbour in node_neighbours:
                neighbor_amounts += graph.get_node_degree(node=neighbour)
            nodes_importance[node] = node_degree / neighbor_amounts  # finding hub power of each node
        return nodes_importance

    def method_two(self, nodes, graph):  # RDC
        nodes_importance = dict()
        for node in nodes:
            node_neighbours = graph.get_node_neighbours(node=node)
            rdc = 0
            for neighbour in node_neighbours:
                rdc += 1 / graph.get_node_degree(node=neighbour)
            nodes_importance[node] = rdc  # finding hub power of each node
        return nodes_importance
