from graph import Graph
from hub_lpa import HubLpa
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
        lpa = HubLpa(g)
        lpa.perform_algorithm()
        g.draw_graph()
        print('results for dataset : ', data_set)
        print("NMI :   ",
              normalized_mutual_info_score(get_real_results(ground_truth_data[data_set_counter]), calculate_nmi()))
        print("MOD :   ", g.calculate_modularity())
        print('\n' * 1)
        data_set_counter += 1
