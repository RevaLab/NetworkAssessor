
def find_nodes_unique_to_pathways(node_list, pathway_list, db_pathways, user_pathways):
    nodes_just_from_each_pathway = {}
    for pathway in pathway_list:
        # subtract each instance of pathway nodes from pathway_list
        try:
            pw_nodes = db_pathways[pathway]
        except KeyError:
            pw_nodes = user_pathways[pathway]['genes']
        for node in pw_nodes:
            # If the node has only been added to the list once, that means it's only coming
            # from the pathway and not from query list or other pathways
            if node_list.count(node) == 1:
                try:
                    nodes_just_from_each_pathway[pathway].append(node)
                except KeyError:
                    nodes_just_from_each_pathway[pathway] = [node]
    return nodes_just_from_each_pathway
