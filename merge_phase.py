from graph import Graph


def merge_algorithm(graph: Graph):
    nodes = graph.get_nodes()

    # => O(n)
    communities = get_communities(nodes, graph)

    # => O(c)
    small_communities = get_small_communities(nodes, communities)
    large_communities = get_large_communities(nodes, communities)

    # => O(s_nodes * k)
    # small_communities_with_inner_edge = get_small_community_inner_edge(
    #     small_community_target_nodes(small_communities, graph), graph)

    # current_small_community = small_communities_with_inner_edge[list(small_communities_with_inner_edge.keys())[0]]

    # => O(l_nodes)
    # current_large_community = large_community_target_nodes(large_communities, graph)

    condition = True
    iter_limitation = len(small_communities)
    item_key = 0

    small_community_label = list(small_communities.keys())[item_key]
    small_community = small_communities[small_community_label]
    target_node = small_community_target_nodes(small_community, graph)
    inner_edge = get_small_community_inner_edge(small_community, small_community_label, graph)

    target_node_of_large_communities = large_community_target_nodes(large_communities, graph)

    while condition:
        # => O(c)
        large_community_label = return_largest_dcn(target_node, target_node_of_large_communities, graph)
        # => O(s_nodes*k)
        need_to_update_list = merging_list(small_community, large_community_label, inner_edge, graph)

        if need_to_update_list:
            # => O(s_nodes) -> worst scenario
            merging_operation(need_to_update_list, graph)

            communities[large_community_label] += need_to_update_list[large_community_label]
            communities.pop(small_community_label)

            # => O(c)
            small_communities = get_small_communities(nodes, communities)
            large_communities = get_large_communities(nodes, communities)

            iter_limitation = len(small_communities)
            item_key = 0
            small_community_label = list(small_communities.keys())[item_key]
            small_community = small_communities[small_community_label]
            target_node = small_community_target_nodes(small_community, graph)
            inner_edge = get_small_community_inner_edge(small_community, small_community_label, graph)

            target_node_of_large_communities = large_community_target_nodes(large_communities, graph)
        else:
            item_key += 1
            if len(small_communities) > item_key:
                small_community_label = list(small_communities.keys())[item_key]
                small_community = small_communities[small_community_label]
                target_node = small_community_target_nodes(small_community, graph)
                inner_edge = get_small_community_inner_edge(small_community, small_community_label, graph)

                target_node_of_large_communities = large_community_target_nodes(large_communities, graph)
            iter_limitation -= 1
        if iter_limitation == 0:
            condition = False


def calculate_dcn(node_v, node_i, graph: Graph):  # this is really ok
    degree = graph.get_node_degree(node_v)
    neighbors_of_v = graph.get_node_neighbours(node_v)
    neighbors_of_i = graph.get_node_neighbours(node_i)
    common_neighbors_count = len(set(neighbors_of_v).intersection(neighbors_of_i))

    return degree + (2 * common_neighbors_count)


def return_largest_dcn(target_node, large_community_with_target_node, graph: Graph):
    max_dcn = 0
    largest_dcn = None
    for large_community_label in large_community_with_target_node:
        calculated_dcn = calculate_dcn(target_node, large_community_with_target_node[large_community_label], graph)
        if calculated_dcn > max_dcn:
            largest_dcn = large_community_label
            max_dcn = calculated_dcn
    return largest_dcn


def get_small_community_inner_edge(small_community, small_community_label, graph: Graph):
    counter = 0
    # print(small_community)
    for member in small_community:
        neighbors = graph.get_node_neighbours(member)
        # print(neighbors)
        for neighbor in neighbors:
            if graph.get_node_current_label(neighbor) == small_community_label:
                counter += 1
    return counter / 2


def get_outer_edge(nodes, label, graph: Graph):
    # print(nodes)
    counter = 0
    for node in nodes:
        for neighbor in graph.get_node_neighbours(node):
            if graph.get_node_current_label(neighbor) == label:
                counter += 1
    return counter


def merging_ability(inner_edge, outer_edge):
    # print(inner_edge, outer_edge)
    if (inner_edge / 2) < outer_edge:
        return True
    else:
        return False


def merging_list(merge_candidates, large_community_label, inner_edge, graph: Graph):
    need_to_update_list = dict()
    if merging_ability(inner_edge, get_outer_edge(merge_candidates, large_community_label, graph)):
        if large_community_label in need_to_update_list:
            need_to_update_list[large_community_label] += merge_candidates
        else:
            need_to_update_list[large_community_label] = merge_candidates

    return need_to_update_list


def merging_operation(merge_list, graph: Graph):
    for label in merge_list:
        for node in merge_list[label]:
            graph.set_label_to_node(label, node)


def small_community_target_nodes(small_community, graph: Graph):
    candidate_for_target_node_degree = 0
    for node in small_community:
        node_degree = graph.get_node_degree(node)
        if node_degree >= candidate_for_target_node_degree:
            candidate_for_target_node = node
            candidate_for_target_node_degree = node_degree
    return candidate_for_target_node


def all_communities_with_target_nodes(communities, graph: Graph):
    communities_with_target_node = dict()

    for community in communities:
        candidate_for_target_node_degree = 0
        for node in communities[communities]:
            node_degree = graph.get_node_degree(node)
            if node_degree >= candidate_for_target_node_degree:
                target_node = node
                candidate_for_target_node_degree = node_degree

    return target_node


def large_community_target_nodes(large_communities, graph: Graph):
    large_community_containing_target_nodes = dict()  # one node from each large community with the biggest degree
    for large_community in large_communities:
        candidate_for_large_node_degree = 0
        for large_node in large_communities[large_community]:
            if graph.get_node_degree(large_node) >= candidate_for_large_node_degree:
                candidate_for_large_node = large_node
                candidate_for_large_node_degree = graph.get_node_degree(large_node)
        large_community_containing_target_nodes[large_community] = candidate_for_large_node
    return large_community_containing_target_nodes


def get_communities(nodes, graph: Graph):
    communities = dict()
    for node in nodes:  # => O(n)
        node_current_label = graph.get_node_current_label(node)
        if node_current_label not in communities:
            communities[node_current_label] = [node]
        else:
            communities[node_current_label].append(node)
    # print(communities)
    return communities


def get_small_communities(nodes, communities):
    avg = len(nodes) / len(communities)  # average node in initial communities
    small_communities = dict()  # communities with nodes less than avg
    for community in communities:  # => O(C)
        if len(communities[community]) < avg:
            small_communities[community] = communities[community]
    return small_communities


def get_large_communities(nodes, communities):
    avg = len(nodes) / len(communities)  # average node in initial communities
    large_communities = dict()  # communities with nodes more than or equal to avg
    for community in communities:  # => O(C)
        if len(communities[community]) >= avg:
            large_communities[community] = communities[community]
    return large_communities
