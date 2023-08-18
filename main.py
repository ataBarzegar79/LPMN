import time
import json
from graph import Graph
from hub_lpa import HubLpa
from sklearn.metrics.cluster import normalized_mutual_info_score


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
