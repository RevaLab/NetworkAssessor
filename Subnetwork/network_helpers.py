import networkx as nx
import pickle


def get_next_degree(center, whole_subgraph):
    next_degree_nodes = list(center)

    for gene in center:
        try:
            next_degree_nodes += whole_subgraph.neighbors(gene)
        except nx.exception.NetworkXError:
            pass
    next_degree_sub = nx.Graph(whole_subgraph.subgraph(next_degree_nodes))
    next_degree_sub.remove_nodes_from(list(nx.isolates(next_degree_sub)))

    return next_degree_sub


"""
Output: 
{
    pathway: {
        length: int,
        edges: int,
        nodes: int
    }
}
"""


def get_pathway_counts(graph):
    # Get entire interaction database
    # For each pathway, calculate the subgraph
    # For all nodes in pathway, sum total nearest neighbors
    pathway_counts = {}

    pathways = pickle.load(open('static/important_pathways.pkl', 'rb'))



