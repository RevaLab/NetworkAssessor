from bisect import bisect_left


def calculate_network_pathway_pval(inter_pw_subgraph_edges, query_genes, pathway, all_pw_distribution):
    normalized_inter_pw_subgraph_edges = inter_pw_subgraph_edges / len(query_genes)
    pw_distribution = all_pw_distribution[pathway]

    rank = 100000 - bisect_left(pw_distribution, normalized_inter_pw_subgraph_edges)
    p_val = rank / float(len(pw_distribution))
    return p_val


def calculate_all_pathways_p_vals(pathways_edge_counts, query_genes, all_pw_distribution):

    pathways_p_vals = {}

    for pathway in pathways_edge_counts:
        inter_pw_subgraph_edges = pathways_edge_counts[pathway]
        if pathway in all_pw_distribution:
            pw_distribution = all_pw_distribution[pathway]
        else:
            continue
        normalized_inter_pw_subgraph_edges = inter_pw_subgraph_edges / len(query_genes)

        rank = len(pw_distribution) - bisect_left(pw_distribution, normalized_inter_pw_subgraph_edges)

        p_val = rank / float(len(pw_distribution))

        pathways_p_vals[pathway] = p_val

    return pathways_p_vals
