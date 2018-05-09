from bisect import bisect_left

import networkx as nx


def calculate_internal_p_val(query_genes, interaction_db, db_distribution):
    query_genes_subgraph = nx.Graph(interaction_db.subgraph(query_genes))
    internal_edges = len(query_genes_subgraph.edges())
    internal_nodes = len(query_genes_subgraph.nodes())
    normalized_internal_edges = internal_edges / internal_nodes

    rank = len(db_distribution) - bisect_left(db_distribution, normalized_internal_edges)
    p_val = rank / float(len(db_distribution))
    return p_val
