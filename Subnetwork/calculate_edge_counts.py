"""
For new pathways:
    maintain the previously calculated edge count
For maintained pathways:
    calculate new edge count between current pathway and all other nodes, except for the pathway-exclusive nodes
    Must remove pathway exclusive node, or else pathway will calculate
    more edges with its own nodes
"""


def find_all_other_pathways_nodes(pathway, selected_pathways, db_pathways, user_pathways):
    all_other_pathways_nodes = []
    for other_pathway in selected_pathways:
        if pathway == other_pathway:
            continue

        if other_pathway in db_pathways:
            other_pw_nodes = db_pathways[other_pathway]
        else:
            other_pw_nodes = user_pathways[other_pathway]

        all_other_pathways_nodes += other_pw_nodes
    return all_other_pathways_nodes


def find_pathway_exclusive_nodes(pathway, selected_pathways, db_pathways, user_pathways):
    if pathway in db_pathways:
        pw_nodes = db_pathways[pathway]
    else:
        pw_nodes = user_pathways[pathway]

    all_other_pathways_nodes = find_all_other_pathways_nodes(pathway, selected_pathways, db_pathways, user_pathways)

    pathway_exclusive_nodes = [node for node in pw_nodes if node not in all_other_pathways_nodes]

    return pathway_exclusive_nodes


def subgraph_without_pathway(subgraph, pathway_exclusive_nodes, query_genes):
    subgraph = [node for node in subgraph if node not in pathway_exclusive_nodes]
    return subgraph + query_genes