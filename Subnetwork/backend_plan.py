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


def find_edges_from_current_graph(current_graph, degree):
    if 'edges' not in current_graph['first_degree']['elements']:
        return []

    current_graph_edges = []
    for edge in current_graph[degree]['elements']['edges']:
        current_graph_edges.append(edge['data']['source'])
        current_graph_edges.append(edge['data']['target'])
    return list(set(current_graph_edges))


def find_maintained_pathway_nodes_in_center(center, maintained_pathways, db_pathways, user_pathways):
    # Add back maintained pathway nodes that may have been removed
    # Keeps one degree too many
    all_nodes_from_maintained_pathways_in_center = []
    for pathway in maintained_pathways:
        if pathway == 'query_list':
            continue
        if pathway in db_pathways:
            pw_nodes = db_pathways[pathway]
        else:
            pw_nodes = user_pathways[pathway]['genes']
        for node in pw_nodes:
            if node in center:
                all_nodes_from_maintained_pathways_in_center.append(node)

    return all_nodes_from_maintained_pathways_in_center


def delete_removed_pathway_nodes_from_center(center,
                                             removed_pathways,
                                             db_pathways,
                                             user_pathways):
    # center_with_only_current_pathways = []
    all_nodes_from_removed_pathways = []

    for pathway in removed_pathways:
        # print(pathway)
        if pathway in db_pathways:
            pw_nodes = db_pathways[pathway]
        else:
            pw_nodes = user_pathways[pathway]['genes']
        for node in pw_nodes:
            # this means it's not in both previous edges and query list
            if center.count(node) == 1:
                all_nodes_from_removed_pathways.append(node)
    center_with_only_current_pathways = [node for node in center if node not in all_nodes_from_removed_pathways]
    return center_with_only_current_pathways


def find_new_center(query_genes, current_graph, degree, removed_pathways, maintained_pathways, db_pathways, user_pathways):
    current_graph_edges = find_edges_from_current_graph(current_graph, degree)
    # print("QUERY GENES IN FIND NEW CENTER??")
    # print(len(query_genes))
    new_center = query_genes + current_graph_edges
    all_nodes_from_maintained_pathways_in_center = find_maintained_pathway_nodes_in_center(new_center,
                                                                                           maintained_pathways,
                                                                                           db_pathways,
                                                                                           user_pathways)
    new_center_with_old_pathways_removed = delete_removed_pathway_nodes_from_center(new_center,
                                                                                    removed_pathways,
                                                                                    db_pathways,
                                                                                    user_pathways)
    # What if a node is in a pathway that is removed and a pathway that is kept,
    # but not in the query list:
    # add back maintained pathway nodes that were in the center

    final_new_center = list(set(new_center_with_old_pathways_removed + all_nodes_from_maintained_pathways_in_center))
    return final_new_center


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


def create_whole_graph_with_node_list(interaction_db, all_nodes_for_subgraph):
    return nx.Graph(interaction_db.subgraph(all_nodes_for_subgraph))


def get_next_degree(center, whole_subgraph):
    next_degree_nodes = list(center)

    for gene in center:
        try:
            next_degree_nodes += whole_subgraph.neighbors(gene)
        except nx.exception.NetworkXError:
            pass
    next_degree_sub = nx.Graph(whole_subgraph.subgraph(next_degree_nodes))

    return next_degree_sub


def make_three_degrees_of_graphs(center, whole_graph):

    first_degree_sub = get_next_degree(center, whole_graph)
    first_degree_nodes = list(first_degree_sub.nodes())
    second_degree_sub = get_next_degree(first_degree_nodes, whole_graph)
    second_degree_nodes = list(second_degree_sub.nodes())
    third_degree_sub = get_next_degree(second_degree_nodes, whole_graph)
    third_degree_nodes = list(third_degree_sub.nodes())

    subnetworks = {
        'first': {
            'subnetwork': first_degree_sub,
            'nodes': first_degree_nodes
        },
        'second': {
            'subnetwork': second_degree_sub,
            'nodes': second_degree_nodes
        },
        'third': {
            'subnetwork': third_degree_sub,
            'nodes': third_degree_nodes
        },
    }

    return subnetworks
