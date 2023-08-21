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
        # self.check_mergeability()
        return counter

    def get_important_nodes(self, nodes):
        priority = Priority()
        return priority.give_nodes_priority(self.graph)

    def get_new_label_of_node(self, node: int) -> int:
        label_update = LabelUpdate()
        return label_update.retrieve_new_label(node, self.graph)

    def calculate_dcn(self, node_v, node_i):  # this is really ok
        degree = self.graph.get_node_degree(node_v)
        neighbors_of_v = self.graph.get_node_neighbours(node_v)
        neighbors_of_i = self.graph.get_node_neighbours(node_i)
        common_neighbors_count = len(set(neighbors_of_v).intersection(neighbors_of_i))

        return degree + (2 * common_neighbors_count)

    def return_largest_dcn(self, list1, list2):
        dcn_values = dict()
        for l1 in list1:
            max_dcn = 0
            for l2 in list2:
                if self.calculate_dcn(l1, l2) >= max_dcn:
                    dcn_values[list1[l1]] = list2[l2]
        return dcn_values

    def get_inner_edge(self, node):
        target_node_current_label = self.graph.get_node_current_label(node)
        target_node_neighbors = self.graph.get_node_neighbours(node)
        counter = 0
        for neighbor in target_node_neighbors:
            if self.graph.get_node_current_label(node) == target_node_current_label:
                counter += 1
        return counter

    def get_outer_edge(self, node_v, node_i):
        target_node_v_current_label = self.graph.get_node_current_label(node_v)
        target_node_i_current_label = self.graph.get_node_current_label(node_i)
        all_nodes_in_node_v_community = {node_v}
        for node in self.graph.get_nodes():
            if self.graph.get_node_current_label(node) == target_node_v_current_label:
                all_nodes_in_node_v_community.add(node)
        all_nodes_in_node_i_community = {node_i}
        for node in self.graph.get_nodes():
            if self.graph.get_node_current_label(node) == target_node_i_current_label:
                all_nodes_in_node_i_community.add(node)
        counter = 0
        for target_node_v in all_nodes_in_node_v_community:
            for target_node_i in all_nodes_in_node_i_community:
                if target_node_i in self.graph.get_node_neighbours(target_node_v):
                    counter += 1
        return counter

    def merging_ability(self, inner_edge, outer_edge):
        # print(inner_edge, outer_edge)
        if (inner_edge / 1.2) - outer_edge <= 1:
            return True
        else:
            return False

    def merging_operation(self, merge_candidate_nodes):
        for candidate in merge_candidate_nodes:
            candidate_label = self.graph.get_node_current_label(candidate)
            label_of_large_community = self.graph.get_node_current_label(merge_candidate_nodes.get(candidate))
            all_nodes_in_candidate_community = {candidate}
            for node in self.graph.get_nodes():
                if self.graph.get_node_current_label(node) == candidate_label:
                    all_nodes_in_candidate_community.add(node)
            if self.merging_ability(self.get_inner_edge(candidate),
                                    self.get_outer_edge(candidate, merge_candidate_nodes.get(candidate))):
                for candidate_node in all_nodes_in_candidate_community:
                    self.graph.set_label_to_node(label_of_large_community, candidate_node)

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
            for small_node in small_communities[small_community]:
                if self.graph.get_node_degree(small_node) >= candidate_for_target_node_degree:
                    candidate_for_target_node = small_node
                    candidate_for_target_node_degree = self.graph.get_node_degree(small_node)
            small_community_target_nodes[small_community] = candidate_for_target_node

        large_community_target_nodes = dict()  # one node from each large community with the biggest degree
        for large_community in large_communities:
            candidate_for_large_node_degree = 0
            for large_node in large_communities[large_community]:
                if self.graph.get_node_degree(large_node) >= candidate_for_large_node_degree:
                    candidate_for_large_node = large_node
                    candidate_for_large_node_degree = self.graph.get_node_degree(large_node)
            large_community_target_nodes[large_community] = candidate_for_large_node

        merge_candidate_nodes = self.return_largest_dcn(small_community_target_nodes, large_community_target_nodes)

        self.merging_operation(merge_candidate_nodes)
