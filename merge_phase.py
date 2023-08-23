from graph import Graph


def merge_algorithm(graph: Graph):
    nodes = graph.get_nodes()
    communities = get_communities(nodes, graph)

    small_communities = get_small_communities(nodes, communities)
    large_communities = get_large_communities(nodes, communities)

    # => O(s_nodes * k)
    small_communities_with_inner_edge = set_small_community_inner_edge(
        small_community_target_nodes(small_communities, graph), graph)

    # for s_community in small_communities_with_inner_edge:
    current_small_community = small_communities_with_inner_edge[list(small_communities_with_inner_edge.keys())[0]]
    current_large_community = large_community_target_nodes(large_communities, graph)
    condition = True
    iter_limitation = len(small_communities)
    item_key = 0
    # print("0:", small_communities)
    while condition:
        # => O(c)
        small_community_with_merge_candidate = return_largest_dcn(current_small_community, current_large_community,
                                                                  graph)

        # => O(s_nodes*k)
        need_to_update_list = merging_list(small_community_with_merge_candidate, graph)

        if need_to_update_list:
            # => O(s_nodes) -> worst scenario
            merging_operation(need_to_update_list, graph)

            communities = get_communities(nodes, graph)

            small_communities = get_small_communities(nodes, communities)
            large_communities = get_large_communities(nodes, communities)
            small_communities_with_inner_edge = set_small_community_inner_edge(
                small_community_target_nodes(small_communities, graph), graph)

            if len(small_communities_with_inner_edge) > item_key:
                current_small_community = small_communities_with_inner_edge[
                    list(small_communities_with_inner_edge.keys())[item_key]]
            current_large_community = large_community_target_nodes(large_communities, graph)
            iter_limitation = len(small_communities)
            item_key = 0
            # print(current_large_community)
            # print("1:", small_communities)
        else:
            item_key += 1
            if len(small_communities_with_inner_edge) > item_key:
                current_small_community = small_communities_with_inner_edge[
                    list(small_communities_with_inner_edge.keys())[item_key]]
            iter_limitation -= 1
        if iter_limitation == 0:
            condition = False


def calculate_dcn(node_v, node_i, graph: Graph):  # this is really ok
    degree = graph.get_node_degree(node_v)
    neighbors_of_v = graph.get_node_neighbours(node_v)
    neighbors_of_i = graph.get_node_neighbours(node_i)
    common_neighbors_count = len(set(neighbors_of_v).intersection(neighbors_of_i))

    return degree + (2 * common_neighbors_count)


def return_largest_dcn(list1, list2, graph: Graph):
    max_dcn = 0
    for l2 in list2:
        calculated_dcn = calculate_dcn(list1[1], list2[l2], graph)
        if calculated_dcn > max_dcn:
            max_dcn = calculated_dcn
            length = len(list1)
            if length == 3:
                list1.append([l2, list2[l2]])
            else:
                list1[length - 1] = [l2, list2[l2]]
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
    # print(nodes)
    counter = 0
    for node in nodes:
        for neighbor in graph.get_node_neighbours(node):
            if graph.get_node_current_label(neighbor) == label:
                counter += 1
    return counter


def merging_ability(inner_edge, outer_edge):
    # print(inner_edge, outer_edge)
    if (inner_edge / 2) - outer_edge < 0:
        return True
    else:
        return False


def merging_list(merge_candidates, graph: Graph):
    need_to_update_list = dict()
    label_of_large_community = merge_candidates[3][0]
    all_nodes_in_candidate_community = merge_candidates[0]
    if merging_ability(merge_candidates[2],
                       get_outer_edge(all_nodes_in_candidate_community, label_of_large_community, graph)):
        if label_of_large_community in need_to_update_list:
            need_to_update_list[label_of_large_community] += merge_candidates[0]
        else:
            need_to_update_list[label_of_large_community] = merge_candidates[0]

    return need_to_update_list


def merging_operation(merge_list, graph: Graph):
    for label in merge_list:
        for node in merge_list[label]:
            graph.set_label_to_node(label, node)


def small_community_target_nodes(small_communities, graph: Graph):
    small_community_containing_target_nodes = dict()  # one node from each small community with the biggest degree
    for small_community in small_communities:
        candidate_for_target_node_degree = 0
        small_community_containing_target_nodes[small_community] = [small_communities[small_community]]
        for small_node in small_communities[small_community]:
            if graph.get_node_degree(small_node) >= candidate_for_target_node_degree:
                candidate_for_target_node = small_node
                candidate_for_target_node_degree = graph.get_node_degree(small_node)
        small_community_containing_target_nodes[small_community].append(candidate_for_target_node)
    return small_community_containing_target_nodes


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
