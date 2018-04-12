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


def find_pathway_edge_count(per_pathway_node_list, query_genes, interaction_db):
    pathway_edge_counts = {
        'first_degree': 0,
        'second_degree': 0,
        'third_degree': 0
    }
    per_pathway_subgraph = nx.Graph(interaction_db.subgraph(per_pathway_node_list))

    per_pathway_first_degree_sub = get_next_degree(query_genes, per_pathway_subgraph)
    per_pathway_second_degree_sub = get_next_degree(per_pathway_first_degree_sub.nodes(), per_pathway_subgraph)
    per_pathway_third_degree_sub = get_next_degree(per_pathway_second_degree_sub.nodes(), per_pathway_subgraph)

    pathway_edge_counts['first_degree'] = len(per_pathway_first_degree_sub.edges())
    pathway_edge_counts['second_degree'] = len(per_pathway_second_degree_sub.edges())
    pathway_edge_counts['third_degree'] = len(per_pathway_third_degree_sub.edges())
    # pathways_edge_counts[pathway] = pathway_edge_counts
    return pathway_edge_counts
