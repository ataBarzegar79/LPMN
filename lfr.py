import networkx as nx


class Lfr:
    def __init__(self, lfr_file_path: str, truth_file_path: str):
        self.file_path = lfr_file_path
        self.truth_file_path = truth_file_path
        self.raw_data = self.initialize_networkx_graph()

    def initialize_networkx_graph(self):
        raw_data = []
        with open(self.file_path, 'r') as file:
            for line in file:
                values = line.strip().split('\t')
                if len(values) == 2:
                    raw_data.append((int(values[0]), int(values[1])))
        return raw_data

    def produce_base_network(self):
        base_network = nx.Graph()
        base_network.add_edges_from(self.raw_data)
        return base_network

    def get_truth_of_lpr(self):
        truth = []
        with open(self.truth_file_path, 'r') as file:
            for line in file:
                values = line.strip().split()
                truth.append(int(values[1]))
        return truth
