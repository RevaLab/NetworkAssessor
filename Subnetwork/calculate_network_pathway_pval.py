from bisect import bisect_left

from .network_utils import Parameter


def calculate_network_pathway_pval(inter_pw_subgraph_edges, subgraph_nodes, pathway, db, all_pw_distribution):
    # inter_ql_pw_edges = Parameter.edge_cross(pw_nodes, ql_nodes, db)
    normalized_inter_pw_subgraph_edges = inter_pw_subgraph_edges / len(subgraph_nodes)
    pw_distribution = all_pw_distribution[pathway]

    rank = 100000 - bisect_left(pw_distribution, normalized_inter_pw_subgraph_edges)
    p_val = rank / float(len(pw_distribution))
    return p_val
