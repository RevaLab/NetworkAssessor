
def create_node_list(query_genes, pathway_list, db_pathways, user_pathways):
    node_list = list(query_genes)

    # Add pathway genes to node list
    for pathway in pathway_list:
        try:
            pw_nodes = db_pathways[pathway]
        except KeyError:
            pw_nodes = user_pathways[pathway]['genes']
        node_list += pw_nodes

    return node_list
