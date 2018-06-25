"""
For generating the graph:
 Get new center
    new_center = query_list + current_graph_nodes_with_edges
 Add all nodes of new pathways
    all_nodes_to_consider = current_center + all_new_pathway_nodes
    first_degree_subgraph = networkx.Graph(all_nodes_to_consider)

For calculating edges:
 If pathway is a new pathway:
    keep previously calculated edges
 Else:
    remove pathway only nodes from first_degree_nodes
    then recalculate edges between pw nodes and graph without pathway nodes
        Accounts for multiple new pathways
"""
import networkx as nx
from .network_utils import Parameter
from networkx.readwrite import json_graph


from .list_utils import *


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


def collect_all_nodes_for_subgraph(center, pathways_to_add, db_pathways, user_pathways):
    all_nodes_for_subgraph = list(center)

    # for first degree: center is the center
    # for second degree: center = first_degree_nodes, pathways_to_add = maintained_pathways

    for pathway in pathways_to_add:
        if pathway == 'query_list':
            continue
        if pathway in db_pathways:
            pw_nodes = db_pathways[pathway]
        else:
            pw_nodes = user_pathways[pathway]['genes']
        all_nodes_for_subgraph += pw_nodes

    # all_nodes_for_subgraph += center
    return all_nodes_for_subgraph


def get_next_degree(center, whole_subgraph):
    next_degree_nodes = list(center)

    for gene in center:
        try:
            next_degree_nodes += whole_subgraph.neighbors(gene)
        except nx.exception.NetworkXError:
            pass
    next_degree_sub = nx.Graph(whole_subgraph.subgraph(next_degree_nodes))

    return next_degree_sub


def make_three_degrees_of_graphs(query_genes, whole_graph):

    first_degree_sub = get_next_degree(query_genes, whole_graph)
    first_degree_nodes = list(first_degree_sub.nodes())
    second_degree_sub = get_next_degree(first_degree_nodes, whole_graph)
    second_degree_nodes = list(second_degree_sub.nodes())
    third_degree_sub = get_next_degree(second_degree_nodes, whole_graph)

    subnetworks = {
        'first_degree': json_graph.cytoscape_data(first_degree_sub),
        'second_degree': json_graph.cytoscape_data(second_degree_sub),
        'third_degree': json_graph.cytoscape_data(third_degree_sub),
        'whole': json_graph.cytoscape_data(whole_graph)
    }

    return subnetworks


def calculate_pathway_edge_counts(query_genes, db_pathways, pathway_neighbors):
    pathways_edge_counts = {}
    # all_pathways = list(user_pathways.keys()) + list(db_pathways.keys())
    for pathway in db_pathways:
        # if pathway in db_pathways:
        #     pw_nodes = db_pathways[pathway]
        # else:
        #     pw_nodes = user_pathways[pathway]['genes']

        pw_nodes = db_pathways[pathway]

        query_genes_with_edges_to_pathway = []

        for node in pw_nodes:
            if node in pathway_neighbors[pathway]:
                query_genes_that_are_neighbors_of_this_pw_node = intersect(pathway_neighbors[pathway][node], query_genes)
                query_genes_with_edges_to_pathway += query_genes_that_are_neighbors_of_this_pw_node

        edges = len(query_genes_with_edges_to_pathway)

        if edges:
            pathways_edge_counts[pathway] = edges
        else:
            pathways_edge_counts[pathway] = 0

    return pathways_edge_counts


def assign_user_pathways_to_genes(user_pathways, whole_graph, all_nodes_for_subgraph):
    graph_pathways = nx.get_node_attributes(whole_graph, 'pathways')

    user_pathways_by_gene = normalize_user_pathways_by_gene(user_pathways)
    for gene in user_pathways_by_gene:
        if gene in graph_pathways:
            current_gene_pathways = graph_pathways[gene]
        else:
            current_gene_pathways = []

        if gene in all_nodes_for_subgraph:
            current_gene_pathways += user_pathways_by_gene[gene]
