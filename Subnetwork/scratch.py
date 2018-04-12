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
#     # pathways_edge_counts[pathway] = pathway_edge_counts
#     return pathway_edge_counts