import time

from graph import Graph


def merge_algorithm(graph: Graph, nodes_additional_data):
    for i in range(2):
        iter_start_merge = time.time()

        communities_start = time.time()
        communities = get_communities(nodes_additional_data, nodes_additional_data, graph)

        small_communities = get_small_communities(nodes_additional_data, communities)
        large_communities = get_large_communities(nodes_additional_data, communities)
        target_node_of_large_communities = large_community_target_nodes(large_communities)
        communities_end = time.time()

        # print('communities found in : ', communities_end - communities_start)

        for small_community_label in small_communities:
            small_community = small_communities[small_community_label]
            target_node = small_community[1]

            inner_edge_start = time.time()
            inner_edge_and_large_neighbors = get_small_community_inner_edge(small_community, small_community_label,
                                                                            nodes_additional_data, large_communities,
                                                                            graph)
            inner_edge_end = time.time()
            # print('inner_edge finished in : ', inner_edge_end - inner_edge_start)

            dcn_started = time.time()
            large_community_label = return_largest_dcn(target_node, target_node_of_large_communities,
                                                       inner_edge_and_large_neighbors,
                                                       nodes_additional_data, graph)
            dcn_ended = time.time()

            # print('dcn calculated in : ', dcn_ended - dcn_started)

            merge_list_started = time.time()
            need_to_update_list = merging_list(small_community[0], large_community_label,
                                               inner_edge_and_large_neighbors['inner_edge'],
                                               nodes_additional_data, graph)
            merge_list_ended = time.time()

            # print('merge list founded in : ', merge_list_ended - merge_list_started)

            if need_to_update_list:
                merge_operation_started = time.time()
                merging_operation(need_to_update_list, graph)
                merge_operation_ended = time.time()

                # print('merge operation finished in : ', merge_operation_ended - merge_operation_started)
        iter_end_merge = time.time()
        # print('merging iteration finished in : ', iter_end_merge - iter_start_merge)


def calculate_dcn(node_v, node_i, nodes_additional_data, graph: Graph):  # this is really ok
    degree = nodes_additional_data[node_v]['degree']
    neighbors_of_v = nodes_additional_data[node_v]['neighbours']
    neighbors_of_i = nodes_additional_data[node_i]['neighbours']
    common_neighbors_count = len(set(neighbors_of_v).intersection(neighbors_of_i))

    return degree + (2 * common_neighbors_count)


def return_largest_dcn(target_node, large_community_with_target_node, large_neighbors, nodes_additional_data,
                       graph: Graph):
    max_dcn = 0
    largest_dcn = None
    for large_community_label in large_neighbors['large_neighbors']:
        calculated_dcn = calculate_dcn(target_node, large_community_with_target_node[large_community_label],
                                       nodes_additional_data, graph)
        if calculated_dcn > max_dcn:
            largest_dcn = large_community_label
            max_dcn = calculated_dcn
    return largest_dcn


def get_small_community_inner_edge(small_community, small_community_label, all_nodes_additional_data, large_communities,
                                   graph: Graph):
    counter = 0
    inner_edge_and_neighbor_large_communities = {
        'inner_edge': 0,
        'large_neighbors': set()
    }
    for member in small_community[0]:
        for neighbor in all_nodes_additional_data[member]['neighbours']:
            neighbor_label = graph.get_node_current_label(neighbor)
            if neighbor_label in large_communities:
                inner_edge_and_neighbor_large_communities['large_neighbors'].add(neighbor_label)
            if neighbor_label == small_community_label:
                counter += 1
    inner_edge_and_neighbor_large_communities['inner_edge'] = counter / 2
    return inner_edge_and_neighbor_large_communities


def get_outer_edge(nodes, label, nodes_additional_data, graph: Graph):
    counter = 0

    for node in nodes:
        for neighbor in nodes_additional_data[node]['neighbours']:
            if graph.get_node_current_label(neighbor) == label:
                counter += 1
    return counter


def merging_ability(inner_edge, outer_edge):
    if (inner_edge / 2) < outer_edge:
        return True
    else:
        return False


def merging_list(merge_candidates, large_community_label, inner_edge, nodes_additional_data, graph: Graph):
    need_to_update_list = dict()
    if merging_ability(inner_edge,
                       get_outer_edge(merge_candidates, large_community_label, nodes_additional_data, graph)):
        if large_community_label in need_to_update_list:
            need_to_update_list[large_community_label] += merge_candidates
        else:
            need_to_update_list[large_community_label] = merge_candidates

    return need_to_update_list


def merging_operation(merge_list, graph: Graph):
    for label in merge_list:
        for node in merge_list[label]:
            graph.set_label_to_node(label, node)


def large_community_target_nodes(large_communities):
    large_community_containing_target_nodes = dict()  # one node from each large community with the biggest degree
    for large_community in large_communities:
        large_community_containing_target_nodes[large_community] = large_communities[large_community][1]
    return large_community_containing_target_nodes


def get_communities(nodes, nodes_additional_data, graph: Graph):
    communities = dict()
    for node in nodes:  # => O(n)
        node_current_label = graph.get_node_current_label(node)
        if node_current_label not in communities:
            communities[node_current_label] = [[node]]
        else:
            communities[node_current_label][0].append(node)
    for community in communities:
        candidate_for_target_node_degree = 0
        for node in communities[community][0]:
            node_degree = nodes_additional_data[node]['degree']
            if node_degree >= candidate_for_target_node_degree:
                target_node = node
                candidate_for_target_node_degree = node_degree
        communities[community].append(target_node)
    return communities


def get_small_communities(nodes, communities):
    avg = len(nodes) / len(communities)  # average node in initial communities
    small_communities = dict()  # communities with nodes less than avg
    for community in communities:  # => O(C)
        if len(communities[community][0]) < avg:
            small_communities[community] = communities[community]
    return small_communities


def get_large_communities(nodes, communities):
    avg = len(nodes) / len(communities)  # average node in initial communities
    large_communities = dict()  # communities with nodes more than or equal to avg
    for community in communities:  # => O(C)
        if len(communities[community][0]) >= avg:
            large_communities[community] = communities[community]
    return large_communities
