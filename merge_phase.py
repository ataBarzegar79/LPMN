from graph import Graph


class MergePhase:
    def __init__(self, graph: Graph, additional_data: dict):
        self.community_average_size = None
        self.graph = graph
        self.additional_data = additional_data
        self.nodes = graph.get_nodes()

    def merge_algorithm(self):
        current_communities = self.retrieve_communities()
        self.community_average_size = self.get_community_average_size(current_communities)
        splited_communities = self.split_communities_with_candidate_nodes(current_communities)
        small_communities = splited_communities['small']
        large_communities = splited_communities['large']
        self.set_small_communities_merge_community(small_communities=small_communities,
                                                   large_communities=large_communities)

    def retrieve_communities(self) -> dict:
        communities = dict()
        for node in self.nodes:
            node_label = self.graph.get_node_current_label(node=node)
            if node_label not in communities:
                communities[node_label] = 1
            else:
                communities[node_label] += 1
        return communities

    def get_community_average_size(self, current_communities) -> int:
        return int(len(self.nodes) / len(current_communities))

    def split_communities_with_candidate_nodes(self, current_communities):
        splited_communities = {
            'small': dict(),
            'large': dict()
        }
        for community in current_communities:
            community_nodes = current_communities[community]
            print(community_nodes)
            exit()
            community_size = len(community_nodes)
            if community_size <= self.community_average_size:
                community_extent = 'small'
            else:
                community_extent = 'large'
            splited_communities[community_extent][community] = {
                'nodes': community_nodes,
                'candid_node': self.calculate_initial_community_candid_node(nodes=community_nodes)
            }
        return splited_communities

    def calculate_initial_community_candid_node(self, nodes) -> int:
        maximum_node_degree = (nodes[0], self.graph.get_node_degree(nodes[0]))
        for node in nodes[1:]:
            node_degree = self.graph.get_node_degree(node)
            if node_degree > maximum_node_degree[1]:
                maximum_node_degree = (node, node_degree)
        return maximum_node_degree[0]

    def set_small_communities_merge_community(self, small_communities, large_communities):
        for community in small_communities:
            community_nodes = small_communities[community]['nodes']
            small_community_align_large_communities = set()
            for node in community_nodes:
                node_neighbors = self.additional_data[node]['neighbors']
                for neighbor in node_neighbors:
                    neighbor_label = self.graph.get_node_current_label(node=neighbor)
                    if neighbor_label in large_communities:
                        small_community_align_large_communities.update(neighbor_label)
            max_large_community = (0, 0)
            small_candidate = small_communities[community]['candid_node']
            for large_community in small_community_align_large_communities:
                large_candidate = large_community[large_community]['candid_node']
                mutuality_score = self.find_mutuality_score_between_candidates(c1=small_candidate, c2=large_candidate)
                if mutuality_score > max_large_community[2]:
                    max_large_community = (large_community, mutuality_score)
            if (self.large_community_should_merge_to_small(small_members=community_nodes,
                                                           large_members=large_communities[max_large_community[0]][
                                                               'nodes'])):
                for node in community_nodes:
                    self.graph.set_label_to_node(max_large_community[0], node)

    def find_mutuality_score_between_candidates(self, c1, c2):
        return len(
            set(self.graph.get_node_neighbours(c1)).intersection(self.graph.get_node_neighbours(c2))
        )

    def large_community_should_merge_to_small(self, small_members, large_members):
        count_inner = 0
        count_outer = 0
        for member in small_members:
            for neighbor in self.additional_data[member]['neighbors']:
                if neighbor in small_members:
                    count_inner += 1
                else:
                    if neighbor in large_members:
                        count_outer += 1

        return count_inner / 4 - count_outer <= 1
