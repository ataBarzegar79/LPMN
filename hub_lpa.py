import graph
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
        # self.check_mergeability()
        return counter

    def get_important_nodes(self, nodes):
        # nodes_betweenness = nx.betweenness_centrality(self.graph.graph)
        nodes_importance = dict()
        for node in nodes:
            # node_betweenness = nodes_betweenness[node]
            node_neighbours = self.graph.get_node_neighbours(node=node)
            rdc = 0
            for neighbour in node_neighbours:
                rdc += 1 / self.graph.get_node_degree(node=neighbour)
            nodes_importance[node] = rdc  # finding hub power of each node
        return sorted(nodes_importance.items(), key=lambda x: x[1], reverse=True)

    def get_new_label_of_node(self, node: int) -> int:
        node_neighbors = self.graph.get_node_neighbours(node=node)
        label_count = dict()
        for neighbor in node_neighbors:
            label = self.graph.get_node_current_label(node=neighbor)
            if label not in label_count:
                label_count[label] = 1
            else:
                label_count[label] += 1
        max_value = max(label_count.values())
        labels_with_max_value = [label for label, count in label_count.items() if count == max_value]
        if len(labels_with_max_value) > 1:
            return self.get_most_appreciate_label(node_neighbors)
        else:
            return labels_with_max_value[0]

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
            for neighbor in node_neighbors:
                neighbor_degree = self.graph.get_node_degree(neighbor)
                if neighbor_degree > max_degree_neighbor[1]:
                    max_degree_neighbor = (neighbor, neighbor_degree)
            return self.graph.get_node_current_label(max_degree_neighbor[0])
        else:
            return self.graph.get_node_current_label(neighbors_with_maximum_score[0])

    def calculate_dcn(self, node_v, node_i):  # this is really ok
        degree = self.graph.get_node_degree(node_v)
        neighbors_of_v = self.graph.get_node_neighbours(node_v)
        neighbors_of_i = self.graph.get_node_neighbours(node_i)
        common_neighbors_count = len(set(neighbors_of_v).intersection(neighbors_of_i))

        return degree + (2 * common_neighbors_count)

    def return_largest_dcn(self, list1, list2):
        for l1 in list1:
            max_dcn = 0
            for l2 in list2:
                if self.calculate_dcn(list1[l1][1], list2[l2]) >= max_dcn:
                    length = len(list1[l1])
                    if length == 3:
                        list1[l1].append([l2, list2[l2]])
                    else:
                        list1[l1][length - 1] = [l2, list2[l2]]
        return list1

    def get_inner_edge(self, node):
        target_node_current_label = self.graph.get_node_current_label(node)
        target_node_neighbors = self.graph.get_node_neighbours(node)
        counter = 0
        for neighbor in target_node_neighbors:
            if self.graph.get_node_current_label(node) == target_node_current_label:
                counter += 1
        return counter

    def set_small_community_inner_edge(self, small_communities):
        counter = 0
        for small_community in small_communities:
            for member in small_communities[small_community][0]:
                neighbors = self.graph.get_node_neighbours(member)
                for neighbor in neighbors:
                    if self.graph.get_node_current_label(neighbor) == small_community:
                        counter += 1
            small_communities[small_community].append(counter / 2)
        return small_communities

    def get_outer_edge(self, nodes, label):
        counter = 0
        for node in nodes:
            for neighbor in self.graph.get_node_neighbours(node):
                if self.graph.get_node_current_label(neighbor) == label:
                    counter += 1
        return counter

    def merging_ability(self, inner_edge, outer_edge):
        if (inner_edge / 2) - outer_edge <= 1:
            return True
        else:
            return False

    def merging_list(self, merge_candidates):
        need_to_update_list = dict()
        for candidate in merge_candidates:
            label_of_large_community = merge_candidates[candidate][3][0]
            all_nodes_in_candidate_community = merge_candidates[candidate][0]
            if self.merging_ability(merge_candidates[candidate][2],
                                    self.get_outer_edge(all_nodes_in_candidate_community, label_of_large_community)):
                need_to_update_list[label_of_large_community] = merge_candidates[candidate][0]
        return need_to_update_list

    def merging_operation(self, merging_list):
        for label in merging_list:
            for node in merging_list[label]:
                self.graph.set_label_to_node(label, node)

    def check_mergeability(self):
        communities = dict()
        nodes = self.graph.get_nodes()
        for node in nodes:  # => O(n)
            node_current_label = self.graph.get_node_current_label(node)
            if node_current_label not in communities:
                communities[node_current_label] = [node]
            else:
                communities[node_current_label].append(node)

        avg = len(nodes) / len(communities)  # average node in initial communities
        small_communities = dict()  # communities with nodes less than avg
        large_communities = dict()  # communities with nodes more than or equal to avg
        for community in communities:  # => O(C)
            if len(communities[community]) >= avg:
                large_communities[community] = communities[community]
            else:
                small_communities[community] = communities[community]

        # => O(n)
        small_community_target_nodes = dict()  # one node from each small community with the biggest degree
        for small_community in small_communities:
            candidate_for_target_node_degree = 0
            small_community_target_nodes[small_community] = [small_communities[small_community]]
            for small_node in small_communities[small_community]:
                if self.graph.get_node_degree(small_node) >= candidate_for_target_node_degree:
                    candidate_for_target_node = small_node
                    candidate_for_target_node_degree = self.graph.get_node_degree(small_node)
            small_community_target_nodes[small_community].append(candidate_for_target_node)

        large_community_target_nodes = dict()  # one node from each large community with the biggest degree
        for large_community in large_communities:
            candidate_for_large_node_degree = 0
            for large_node in large_communities[large_community]:
                if self.graph.get_node_degree(large_node) >= candidate_for_large_node_degree:
                    candidate_for_large_node = large_node
                    candidate_for_large_node_degree = self.graph.get_node_degree(large_node)
            large_community_target_nodes[large_community] = candidate_for_large_node

        # => O(s_nodes * k)
        small_communities_with_inner_edge = self.set_small_community_inner_edge(small_community_target_nodes)

        # => O(c)
        small_communities_with_merge_candidate = self.return_largest_dcn(small_communities_with_inner_edge,
                                                                         large_community_target_nodes)
        # => O(s_nodes*k)
        need_to_update_list = self.merging_list(small_communities_with_merge_candidate)

        # => O(s_nodes) -> worst scenario
        self.merging_operation(need_to_update_list)
