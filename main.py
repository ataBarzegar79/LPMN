from graph import Graph
import networkx as nx
from sklearn.metrics.cluster import normalized_mutual_info_score

datasets = [
    './samples/football.gml',
    './samples/dolphins.gml',
    './samples/karate.gml',
    './samples/polbooks.gml',
]

ground_truth_data = [
    './samples/grand_truth/football_real_labels.txt',
    './samples/grand_truth/dolphins_real_labels.txt',
    './samples/grand_truth/karate_real_labels.txt',
    './samples/grand_truth/polbooks_real_labels.txt',
]


def get_important_nodes():
    nodes = g.get_nodes()
    nodes_betweenness = nx.betweenness_centrality(g.graph)
    nodes_importance = dict()
    for node in nodes:
        node_betweenness = nodes_betweenness[node]
        node_neighbours = g.get_node_neighbours(node=node)
        sum_of_neighbors_degree = 0
        node_degree = g.get_node_degree(node)
        for neighbour in node_neighbours:
            sum_of_neighbors_degree += g.get_node_degree(node=neighbour)
        nodes_importance[node] = (node_degree / sum_of_neighbors_degree) * (1 + node_betweenness)
    return sorted(nodes_importance.items(), key=lambda x: x[1], reverse=True)


def get_maximum_label(node):
    node_neighbors = g.get_node_neighbours(node)
    neighbors_score = dict()
    for neighbor in node_neighbors:
        mutual_neighbors = set(g.get_node_neighbours(node))
        mutual_neighbors.update(g.get_node_neighbours(neighbor))
        neighbors_score[neighbor] = len(mutual_neighbors)
    max_value = max(neighbors_score.values())
    keys_with_max_value = [key for key, value in neighbors_score.items() if value == max_value]
    if len(keys_with_max_value) > 1:
        max_degree_neighbor = (None, 0)
        for neighbor in node_neighbors:
            neighbor_degree = g.get_node_degree(neighbor)
            if neighbor_degree > max_degree_neighbor[1]:
                max_degree_neighbor = (neighbor, neighbor_degree)
        return max_degree_neighbor[0]
    else:
        return keys_with_max_value[0]


def get_new_label_of_node(node):
    node_neighbors = g.get_node_neighbours(node)
    label_count = dict()
    for neighbor in node_neighbors:
        label = g.get_node_current_label(neighbor)
        if label not in label_count:
            label_count[label] = 1
        else:
            label_count[label] += 1
    max_value = max(label_count.values())
    keys_with_max_value = [key for key, value in label_count.items() if value == max_value]
    if len(keys_with_max_value) > 1:
        return get_maximum_label(node)
    else:
        return keys_with_max_value[0]


def check_mergebility():

    pass  # ehsan


def do_the_algorithm():
    nodes = g.get_nodes()
    for node in nodes:
        g.set_label_to_node(label=node, node=node)
    nodes_based_on_importance = get_important_nodes()
    for item in range(10):
        for node in nodes_based_on_importance:
            new_label = get_new_label_of_node(node[0])
            g.set_label_to_node(new_label, node[0])
    check_mergebility()


def calculate_nmi():
    nodes = g.get_nodes()
    predicted_labels = list()
    for node in nodes:
        predicted_labels.append(g.get_node_current_label(node))

    return predicted_labels


def get_real_results(path):
    with open(path, 'r') as file:
        numbers_list = [int(line.strip()) for line in file]
    return numbers_list


if __name__ == "__main__":
    data_set_counter = 0
    for data_set in datasets:
        g = Graph(data_set)
        do_the_algorithm()
        print('results for dataset : ', data_set)
        print("NMI :   ",
              normalized_mutual_info_score(get_real_results(ground_truth_data[data_set_counter]), calculate_nmi()))
        print("MOD :   ", g.calculate_modularity())
        print('\n' * 1)
        data_set_counter += 1
