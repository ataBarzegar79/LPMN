import time
import json
import networkx as nx
from graph import Graph
from hub_lpa import HubLpa
from file_format import FileFormat
from graph_order import GraphOrder
from sklearn.metrics.cluster import normalized_mutual_info_score
from networkx.generators.community import LFR_benchmark_graph
from collections import Counter


def get_real_results(path):
    with open(path, 'r') as file:
        numbers_list = [int(line.strip()) for line in file]
    return numbers_list


def cast_file_format(raw: str) -> FileFormat:
    return [file_format for file_format in FileFormat if file_format.value == raw][0]


def cast_order_format(raw: str) -> GraphOrder:
    return [order for order in GraphOrder if order.value == raw][0]


def load_datasets():
    with open('settings.json') as json_file:
        data = json.load(json_file)['data_sets']
    return {
        dataset_path: {
            'name': data[dataset_path]['name'],
            'file_format': cast_file_format(data[dataset_path]['file_format']),
            'grand_truth_file_path': data[dataset_path]['grand_truth_file_path'],
            'order_format': cast_order_format(data[dataset_path]['order_format']),
            'large_community': data[dataset_path]['large_community']
        } for dataset_path in data if data[dataset_path]['calculate'] == True
    }


def find_predicted_max_communities(graph: Graph):
    nodes = graph.get_nodes()
    communities = dict()
    for node in nodes:
        label = graph.get_node_current_label(node)
        if label not in communities:
            communities[label] = [node]
        else:
            communities[label].append(node)


def rearrange_top_community_truth(file_path: str):
    with open(file_path, 'r') as file:
        communities = [line.strip().split('\t') for line in file]
    arranged_data = list()
    counter = 0
    for community in communities:
        for node in community:
            arranged_data.append((int(node), counter))
        counter += 1
    arranged_data = sorted(arranged_data, key=lambda x: x[0])
    grand_truth = []
    predicted = []
    for data in arranged_data:
        grand_truth.append(data[1])
        predicted.append(graph.get_node_current_label(data[0]))
    return grand_truth, predicted


if __name__ == "__main__":
    datasets = load_datasets()
    for path in datasets:
        graph = Graph(
            graph_file_path=path,
            order_format=datasets[path]['order_format'],
            file_format=datasets[path]['file_format']
        )
        hup_lpa = HubLpa(graph=graph)
        algorithm_start_time = time.time()
        iteration_count = hup_lpa.perform_algorithm()
        algorithm_finish_time = time.time()
        print('data set   : ', datasets[path]['name'])
        print('algorithm executed in  :', algorithm_finish_time - algorithm_start_time)
        print('algorithm iteration count : ', iteration_count)
        print('communities found  : ', len(graph.get_labels()))
        print('gained modularity  :', graph.calculate_modularity())
        if len(datasets[path]['grand_truth_file_path']) > 0:
            if datasets[path]['large_community']:
                predicted_truth = rearrange_top_community_truth(
                    file_path=datasets[path]['grand_truth_file_path']
                )
            else:
                predicted_truth = (get_real_results(datasets[path]['grand_truth_file_path']),
                                   graph.get_graph_labels())
            print('nmi : ',
                  normalized_mutual_info_score(predicted_truth[0], predicted_truth[1])
                  )
        print('------------------------------------------------------' + '\n')

    # lfr

    # MU = 0.1
    # graphs = [
    #     Graph(
    #         LFR_benchmark_graph(5000, min_degree=20, max_degree=50, min_community=20, max_community=50, tau2=2, tau1=2,
    #                             mu=MU), order_format=GraphOrder.NETWORKX_GRAPH, file_format=FileFormat.NETWORKX_GRAPH),
    #     Graph(
    #         LFR_benchmark_graph(5000, min_degree=20, max_degree=50, min_community=20, max_community=100, tau2=2, tau1=2,
    #                             mu=MU), order_format=GraphOrder.NETWORKX_GRAPH, file_format=FileFormat.NETWORKX_GRAPH),
    #     Graph(
    #         LFR_benchmark_graph(10000, min_degree=20, max_degree=50, min_community=20, max_community=50, tau2=2, tau1=2,
    #                             mu=MU), order_format=GraphOrder.NETWORKX_GRAPH, file_format=FileFormat.NETWORKX_GRAPH),
    #     Graph(LFR_benchmark_graph(10000, min_degree=20, max_degree=50, min_community=20, max_community=100, tau2=2,
    #                               tau1=2, mu=MU), order_format=GraphOrder.NETWORKX_GRAPH,
    #           file_format=FileFormat.NETWORKX_GRAPH),
    #     Graph(
    #         LFR_benchmark_graph(20000, min_degree=20, max_degree=50, min_community=20, max_community=50, tau2=2, tau1=2,
    #                             mu=MU), order_format=GraphOrder.NETWORKX_GRAPH, file_format=FileFormat.NETWORKX_GRAPH),
    #     Graph(LFR_benchmark_graph(20000, min_degree=20, max_degree=50, min_community=20, max_community=100, tau2=2,
    #                               tau1=2, mu=MU), order_format=GraphOrder.NETWORKX_GRAPH,
    #           file_format=FileFormat.NETWORKX_GRAPH),
    #     Graph(
    #         LFR_benchmark_graph(50000, min_degree=20, max_degree=50, min_community=20, max_community=50, tau2=2, tau1=2,
    #                             mu=MU), order_format=GraphOrder.NETWORKX_GRAPH, file_format=FileFormat.NETWORKX_GRAPH),
    #     Graph(LFR_benchmark_graph(50000, min_degree=20, max_degree=50, min_community=20, max_community=100, tau2=2,
    #                               tau1=2, mu=MU), order_format=GraphOrder.NETWORKX_GRAPH,
    #           file_format=FileFormat.NETWORKX_GRAPH),
    #     Graph(LFR_benchmark_graph(100000, min_degree=20, max_degree=50, min_community=20, max_community=50, tau2=2,
    #                               tau1=2, mu=MU), order_format=GraphOrder.NETWORKX_GRAPH,
    #           file_format=FileFormat.NETWORKX_GRAPH),
    #     Graph(LFR_benchmark_graph(100000, min_degree=20, max_degree=50, min_community=20, max_community=100, tau2=2,
    #                               tau1=2, mu=MU), order_format=GraphOrder.NETWORKX_GRAPH,
    #           file_format=FileFormat.NETWORKX_GRAPH)
    # ]
    # counter = 1
    # for graph in graphs:
    #     nodes = graph.get_nodes_and_data()
    #     base_nodes = graph.get_nodes()
    #     finded_communities = dict()
    #     community_counter = 0
    #     real_results = []
    #
    #     for node in nodes:
    #         community = node[1]['community']
    #         if community not in finded_communities.values():
    #             finded_communities[community_counter] = community
    #             community_counter += 1
    #             real_results.append(community_counter)
    #         else:
    #             for finded_community in finded_communities.items():
    #                 if finded_community[1] == community:
    #                     real_results.append(finded_community[0])
    #     for node in base_nodes:
    #         if node in graph.get_node_neighbours(node=node):
    #             graph.graph.remove_edge(node, node)
    #
    #     hup_lpa = HubLpa(graph=graph)
    #     algorithm_start_time = time.time()
    #     print('alghorithm start')
    #     iteration_count = hup_lpa.perform_algorithm()
    #     algorithm_finish_time = time.time()
    #     print('data set   : ', 'lfr ', counter)
    #     print('algorithm executed in  :', algorithm_finish_time - algorithm_start_time)
    #     print('algorithm iteration count : ', iteration_count)
    #     print('communities found  : ', len(graph.get_labels()))
    #     print('gained modularity  :', graph.calculate_modularity())
    #     print('gained nmi  : ', normalized_mutual_info_score(
    #         graph.get_graph_labels(),
    #         real_results
    #     ))
    #     print('------------------------------------------------------' + '\n')
    #     counter += 1
