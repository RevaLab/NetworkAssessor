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


def get_pathway_counts(center_nodes, db):
    # query_genes = data['queryGenes']
    # pathway_list = data['pathways']
    # db = data['networkDatabase']

    # load databases
    interaction_db = pickle.load(open('static/{}.pkl'.format(db), 'rb'))
    pathways = pickle.load(open('static/important_pathways.pkl', 'rb'))

    node_list = list(center_nodes)
    # add pathway genes to node list
    # for pathway in pathways:
    pathway = 'WNT_ext_path'
    pathway_nodes = pathways[pathway]
    center_and_pathway = node_list + pathway_nodes
    node_list_with_pathway_genes = list(set(center_and_pathway))
    # print(len(node_list_with_pathway_genes))
    subraph_with_pathway_genes = nx.Graph(interaction_db.subgraph(node_list_with_pathway_genes))
    first_degree_sub = get_next_degree(node_list, subraph_with_pathway_genes)
    edges = list(set(first_degree_sub.edges()))
    # print(len(edges))
    print(pathway)
    print(edges)
