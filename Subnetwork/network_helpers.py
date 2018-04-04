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


def normalize_user_pathways_by_gene(user_pathways):
    user_pathways_by_gene = {}

    for pathway in user_pathways:
        genes = user_pathways[pathway]['genes']

        for gene in genes:
            if gene in user_pathways_by_gene:
                user_pathways_by_gene[gene].append(pathway)
            else:
                user_pathways_by_gene[gene] = [pathway]

    for gene in user_pathways_by_gene:
        user_pathways_by_gene[gene] = list(set(user_pathways_by_gene[gene]))

    return user_pathways_by_gene

