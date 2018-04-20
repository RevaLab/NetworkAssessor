import networkx as nx
from .network_helpers import get_next_degree


def create_three_degrees_of_graph(query_genes, node_list, interaction_db):
    whole_graph = nx.Graph(interaction_db.subgraph(list(set(node_list))))

    first_degree_sub = get_next_degree(query_genes, whole_graph)
    first_degree_nodes = list(first_degree_sub.nodes())
    second_degree_sub = get_next_degree(first_degree_nodes, whole_graph)
    second_degree_nodes = list(second_degree_sub.nodes())
    third_degree_sub = get_next_degree(second_degree_nodes, whole_graph)

    three_degree_graph = {
        'first': first_degree_sub,
        'second': second_degree_sub,
        'third': third_degree_sub
    }

    return three_degree_graph
