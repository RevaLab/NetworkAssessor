import networkx as nx

from .network_utils import Parameter


def get_next_degree(center, whole_subgraph, degree):
    next_degree_nodes = list(center)

    # print("center inside get {} degree".format(degree))
    # print(len(center))
    for gene in center:
        try:
            next_degree_nodes += whole_subgraph.neighbors(gene)
        except nx.exception.NetworkXError:
            pass
    next_degree_sub = nx.Graph(whole_subgraph.subgraph(next_degree_nodes))

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

#

# def find_pathway_edge_count(per_pathway_node_list, query_genes, interaction_db):
#     pathway_edge_counts = {
#         'first_degree': 0,
#         'second_degree': 0,
#         'third_degree': 0
#     }
#     per_pathway_subgraph = nx.Graph(interaction_db.subgraph(per_pathway_node_list))
#
#     per_pathway_first_degree_sub = get_next_degree(query_genes, per_pathway_subgraph)
#     per_pathway_second_degree_sub = get_next_degree(per_pathway_first_degree_sub.nodes(), per_pathway_subgraph)
#     per_pathway_third_degree_sub = get_next_degree(per_pathway_second_degree_sub.nodes(), per_pathway_subgraph)
#
#     pathway_edge_counts['first_degree'] = len(per_pathway_first_degree_sub.edges())
#     pathway_edge_counts['second_degree'] = len(per_pathway_second_degree_sub.edges())
#     pathway_edge_counts['third_degree'] = len(per_pathway_third_degree_sub.edges())
#
#     return pathway_edge_counts


def find_pathway_edge_count(per_pathway_node_list, query_genes, interaction_db, pw_nodes):
    # unique_subgraph_nodes = [node for node in subgraph_nodes if node not in pw_nodes]

    pathway_edge_counts = {
        'first_degree': 0,
        'second_degree': 0,
        'third_degree': 0
    }
    per_pathway_subgraph = nx.Graph(interaction_db.subgraph(per_pathway_node_list))

    per_pathway_first_degree_sub = get_next_degree(query_genes, per_pathway_subgraph)
    per_pathway_second_degree_sub = get_next_degree(per_pathway_first_degree_sub.nodes(), per_pathway_subgraph)
    per_pathway_third_degree_sub = get_next_degree(per_pathway_second_degree_sub.nodes(), per_pathway_subgraph)
    # return Parameter.edge_cross(pw_nodes, unique_subgraph_nodes, interaction_db)
    neighbors_to_pathway = 0
    for node in pw_nodes:
        if node in per_pathway_first_degree_sub.nodes():
            neighbors_to_pathway += len(list(per_pathway_first_degree_sub.neighbors(node)))

    # neighbors_to_pathway = [len(per_pathway_first_degree_sub.neighbors(node)) for node in per_pathway_node_list]
    pathway_edge_counts['first_degree'] = neighbors_to_pathway
    pathway_edge_counts['second_degree'] = len(per_pathway_second_degree_sub.edges())
    pathway_edge_counts['third_degree'] = len(per_pathway_third_degree_sub.edges())
    #
    return pathway_edge_counts
