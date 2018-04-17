"""
Input: Two subgraphs: Query List, Pathway

Output: Normalized num of edges
"""

# Find edges connecting query list and pathway: edges_ql_pw
# ql_nodes = nodes in query list
# ql_edges = links in subgraph query list
# pw_nodes = nodes in pathway
# pw_edges = links in subgraph pathway
# total_subgraph = subgraph(nodes_ql + nodes_pw)
# total_edges = edges(subgraph_ql_pq)
# ql_pw_edges = total_edges - (edges_ql + edges_pw)

# Normalize inter_ql_pw_edges: normalized_inter_ql_pw_edges
# normalized_inter_ql_pw_edges = len(inter_ql_pw_edges) / len(ql_nodes)

# Find rank of edges in pathway-distribution: edges_ql_pw_rank

# Calculate corresponding p-value: ql_pw_edges
# Rank / 100,000
# Edge cases: if rank > 100,000, pVal < calculated p-value (and vice versa)

import pickle


def calculate_network_pathway_pval(ql_nodes, pathway_name, db_name):
    db = pickle.load(open('/Users/calina01/PycharmProjects/go_server_sinai/static/{}.pkl'.format(db_name), 'rb'))
    ql_subgraph = db.subgraph(ql_nodes)
    ql_edges = list(ql_subgraph.edges())
    pathway_network = pickle.load(open('/Users/calina01/PycharmProjects/go_server_sinai/Pathway_network/'
                                       '{}.pkl'.format(pathway_name), 'rb'))
    pw_nodes = list(pathway_network.nodes())
    pw_edges = list(pathway_network.edges())

    total_subgraph = db.subgraph(ql_nodes + pw_nodes)
    total_subgraph_edges = list(total_subgraph.edges())
    intra_ql_pw_edges = ql_edges + pw_edges
    inter_ql_pw_edges = []

    for edge in total_subgraph_edges:
        node_a = edge[0]
        node_b = edge[1]

        # Sometimes edges are reversed tuples
        if (node_a, node_b) in intra_ql_pw_edges or (node_b, node_a) in intra_ql_pw_edges:
            continue

        inter_ql_pw_edges.append(edge)

    normalized_inter_ql_pw_edges = len(inter_ql_pw_edges) / len(ql_nodes)
    pw_distribution = pickle.load(open('/Users/calina01/PycharmProjects/go_server_sinai/'
                                       'Pathway_distribution_sorted/{}.pkl'.format(pathway_name), 'rb'))
    pw_distribution.append(normalized_inter_ql_pw_edges)
    pw_distribution.sort(reverse=True)
    rank = pw_distribution.index(normalized_inter_ql_pw_edges)

    p_val = rank/100000
    return p_val
