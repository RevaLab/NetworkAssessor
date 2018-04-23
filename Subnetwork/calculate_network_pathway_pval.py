from bisect import bisect_left

# from .all_pw_dist import all_pw_dist


def calculate_network_pathway_pval(inter_pw_subgraph_edges, subgraph_nodes, pathway):
    normalized_inter_pw_subgraph_edges = inter_pw_subgraph_edges / len(subgraph_nodes)
    pw_distribution = all_pw_distribution[pathway]

    rank = 100000 - bisect_left(pw_distribution, normalized_inter_pw_subgraph_edges)
    p_val = rank / float(len(pw_distribution))
    return p_val
