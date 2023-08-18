import time
import json

import networkx as nx

from graph import Graph
from hub_lpa import HubLpa
from sklearn.metrics.cluster import normalized_mutual_info_score

from networkx.generators.community import LFR_benchmark_graph
from collections import Counter

def get_real_results(path):
    with open(path, 'r') as file:
        numbers_list = [int(line.strip()) for line in file]
    return numbers_list


available_datasets = {
    'BASE': 'base_datas',
    'LFR': 'lfr',
    'BIG-SCALE': 'big_scale_datas',
}


def load_datasets():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        chosen_dataset = data['data_set_chosen']
        return data['data_sets'][available_datasets[chosen_dataset]]


if __name__ == "__main__":
    datasets = load_datasets().items()
    for dataset, truth in datasets:
        graph = Graph(dataset)
        hup_lpa = HubLpa(graph=graph)
        algorithm_start_time = time.time()
        iteration_count = hup_lpa.perform_algorithm()
        algorithm_finish_time = time.time()

        print('data set   : ', dataset)
        print('algorithm executed in  :', algorithm_finish_time - algorithm_start_time)
        print('algorithm iteration count : ', iteration_count)
        print('communities found  : ', len(graph.get_labels()))
        print('gained modularity  :', graph.calculate_modularity())
        if len(truth) > 0:
            print('gained nmi  : ', normalized_mutual_info_score(
                graph.get_graph_labels(),
                get_real_results(truth)
            ))
        print('------------------------------------------------------' + '\n')

    # lfr

    # graph = Graph(LFR_benchmark_graph(
    #     5000, min_degree=20, max_degree=50, min_community=20, max_community=100, tau2=2, tau1=2, mu=0.7
    # ))
    # nodes = graph.get_nodes_and_data()
    # finded_communities = dict()
    # community_counter = 0
    # real_results = []
    #
    # for node in nodes:
    #     community = node[1]['community']
    #     if community not in finded_communities.values():
    #         finded_communities[community_counter] = community
    #         community_counter += 1
    #         real_results.append(community_counter)
    #     else:
    #         for finded_community in finded_communities.items():
    #             if finded_community[1] == community:
    #                 real_results.append(finded_community[0])
    #
    # hup_lpa = HubLpa(graph=graph)
    # algorithm_start_time = time.time()
    # print('alghorithm start')
    # iteration_count = hup_lpa.perform_algorithm()
    # algorithm_finish_time = time.time()
    # print('data set   : ', 'lfr 500')
    # print('algorithm executed in  :', algorithm_finish_time - algorithm_start_time)
    # print('algorithm iteration count : ', iteration_count)
    # print('communities found  : ', len(graph.get_labels()))
    # print('gained modularity  :', graph.calculate_modularity())
    # if True:
    #     print('gained nmi  : ', normalized_mutual_info_score(
    #         graph.get_graph_labels(),
    #         real_results
    #     ))
    # print('------------------------------------------------------' + '\n')


