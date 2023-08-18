from graph import Graph
from hub_lpa import HubLpa
from sklearn.metrics.cluster import normalized_mutual_info_score
from lfr import Lfr

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
    # data_set_counter = 0
    # for data_set in datasets:
    #     g = Graph(data_set)
    #     lpa = HubLpa(g)
    #     lpa.perform_algorithm()
    #     g.draw_graph()
    #     print('results for dataset : ', data_set)
    #     print("NMI :   ",
    #     print("MOD :   ", g.calculate_modularity())
    #     print('\n' * 1)
    #     data_set_counter += 1
    lfr = Lfr('./samples/lfr/1k-network.dat', './samples/lfr/1k-community.dat')
    g = Graph(lfr.produce_base_network())
    lpa = HubLpa(g)
    lpa.perform_algorithm()
    # g.draw_graph()
    # print(g.calculate_modularity())
    # print(calculate_nmi())
    # print(',,,,,,============')
    # print(lfr.get_truth_of_lpr())
    # exit()
    # g.draw_graph()
    print(g.calculate_modularity())
    print(
        normalized_mutual_info_score(
            calculate_nmi(),
            lfr.get_truth_of_lpr()
        ))
