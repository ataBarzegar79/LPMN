from enum import Enum


class GraphOrder(Enum):
    EDGE_LIST = 'edge-list'
    NEIGHBOR_BASE = 'neighbor-base'
    BASIC_GML = 'basic-gml'
    NETWORKX_GRAPH = 'nx_graph'
