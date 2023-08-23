from graph import Graph


def merge_algorithm(graph: Graph):
    communities = dict()
    nodes = graph.get_nodes()
    for node in nodes:  # => O(n)
        node_current_label = graph.get_node_current_label(node)
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
            if graph.get_node_degree(small_node) >= candidate_for_target_node_degree:
                candidate_for_target_node = small_node
                candidate_for_target_node_degree = graph.get_node_degree(small_node)
        small_community_target_nodes[small_community].append(candidate_for_target_node)

    large_community_target_nodes = dict()  # one node from each large community with the biggest degree
    for large_community in large_communities:
        candidate_for_large_node_degree = 0
        for large_node in large_communities[large_community]:
            if graph.get_node_degree(large_node) >= candidate_for_large_node_degree:
                candidate_for_large_node = large_node
                candidate_for_large_node_degree = graph.get_node_degree(large_node)
        large_community_target_nodes[large_community] = candidate_for_large_node

    # => O(s_nodes * k)
    small_communities_with_inner_edge = set_small_community_inner_edge(small_community_target_nodes, graph)

    # => O(c)
    small_communities_with_merge_candidate = return_largest_dcn(small_communities_with_inner_edge,
                                                                large_community_target_nodes, graph)
    # => O(s_nodes*k)
    need_to_update_list = merging_list(small_communities_with_merge_candidate, graph)

    # => O(s_nodes) -> worst scenario
    merging_operation(need_to_update_list, graph)


def calculate_dcn(node_v, node_i, graph: Graph):  # this is really ok
    degree = graph.get_node_degree(node_v)
    neighbors_of_v = graph.get_node_neighbours(node_v)
    neighbors_of_i = graph.get_node_neighbours(node_i)
    common_neighbors_count = len(set(neighbors_of_v).intersection(neighbors_of_i))

    return degree + (2 * common_neighbors_count)


def return_largest_dcn(list1, list2, graph: Graph):
    for l1 in list1:
        max_dcn = 0
        for l2 in list2:
            calculated_dcn = calculate_dcn(list1[l1][1], list2[l2], graph)
            if calculated_dcn > max_dcn:
                max_dcn = calculated_dcn
                length = len(list1[l1])
                if length == 3:
                    list1[l1].append([l2, list2[l2]])
                else:
                    list1[l1][length - 1] = [l2, list2[l2]]
    return list1


def get_inner_edge(node, graph: Graph):
    target_node_current_label = graph.get_node_current_label(node)
    target_node_neighbors = graph.get_node_neighbours(node)
    counter = 0
    for neighbor in target_node_neighbors:
        if graph.get_node_current_label(node) == target_node_current_label:
            counter += 1
    return counter


def set_small_community_inner_edge(small_communities, graph: Graph):
    counter = 0
    for small_community in small_communities:
        for member in small_communities[small_community][0]:
            neighbors = graph.get_node_neighbours(member)
            for neighbor in neighbors:
                if graph.get_node_current_label(neighbor) == small_community:
                    counter += 1
        small_communities[small_community].append(counter / 2)
    return small_communities


def get_outer_edge(nodes, label, graph: Graph):
    counter = 0
    for node in nodes:
        for neighbor in graph.get_node_neighbours(node):
            if graph.get_node_current_label(neighbor) == label:
                counter += 1
    return counter


def merging_ability(inner_edge, outer_edge):
    if (inner_edge / 2) - outer_edge <= 1:
        return True
    else:
        return False


def merging_list(merge_candidates, graph: Graph):
    need_to_update_list = dict()
    for candidate in merge_candidates:
        label_of_large_community = merge_candidates[candidate][3][0]
        all_nodes_in_candidate_community = merge_candidates[candidate][0]
        if merging_ability(merge_candidates[candidate][2],
                           get_outer_edge(all_nodes_in_candidate_community, label_of_large_community, graph)):
            if label_of_large_community in need_to_update_list:
                need_to_update_list[label_of_large_community] += merge_candidates[candidate][0]
            else:
                need_to_update_list[label_of_large_community] = merge_candidates[candidate][0]

    return need_to_update_list


def merging_operation(merge_list, graph: Graph):
    for label in merge_list:
        for node in merge_list[label]:
            graph.set_label_to_node(label, node)
