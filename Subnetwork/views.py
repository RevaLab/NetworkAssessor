import json
import pickle
import networkx as nx

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .network_helpers import get_next_degree, normalize_user_pathways_by_gene, find_pathway_edge_count
from networkx.readwrite import json_graph


@csrf_exempt
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
    else:
        data = {}
    print(data)
    query_genes = data['userPathways']['query_list']['genes']
    user_pathways = data['userPathways']
    pathway_list = data['pathways'] # all selected pathways
    db = data['networkDatabase']
    # db = data['networkDatabase']

    # load databases
    # db = 'biogrid'
    interaction_db = pickle.load(open('static/{}.pkl'.format(db), 'rb'))
    db_pathways = pickle.load(open('static/important_pathways.pkl', 'rb'))
    node_list = list(query_genes)

    # Add pathway genes to node list
    for pathway in pathway_list:
        try:
            node_list += db_pathways[pathway]
        except KeyError:
            node_list += user_pathways[pathway]['genes']

    # Filter out repeat nodes
    node_list = list(set(node_list))

    # Create whole_graph from node list,
    # which has genes from all selected
    # db_pathways + user_pathways
    whole_graph = nx.Graph(interaction_db.subgraph(node_list))

    pathways_edge_counts = {}

    # get counts for all pathways
    for pathway in db_pathways:
        per_pathway_node_list = node_list + db_pathways[pathway]
        pathway_edge_counts = find_pathway_edge_count(per_pathway_node_list, query_genes, interaction_db)
        pathways_edge_counts[pathway] = pathway_edge_counts

    for pathway in user_pathways:
        per_pathway_node_list = node_list + user_pathways[pathway]['genes']
        pathway_edge_counts = find_pathway_edge_count(per_pathway_node_list, query_genes, interaction_db)
        pathways_edge_counts[pathway] = pathway_edge_counts

    # add user pathways to graph nodes, which may already have pathways
    graph_pathways = nx.get_node_attributes(whole_graph, 'pathways')
    user_pathways_by_gene = normalize_user_pathways_by_gene(user_pathways)
    for gene in user_pathways_by_gene:
        if gene in graph_pathways:
            current_gene_pathways = graph_pathways[gene]
        else:
            current_gene_pathways = []

        if gene in node_list:
            current_gene_pathways += user_pathways_by_gene[gene]
    #
    # # find next degree
    first_degree_sub = get_next_degree(query_genes, whole_graph)
    second_degree_sub = get_next_degree(first_degree_sub.nodes(), whole_graph)
    third_degree_sub = get_next_degree(second_degree_sub.nodes(), whole_graph)

    all_subgraphs = {
        'first_degree': json_graph.cytoscape_data(first_degree_sub),
        'second_degree': json_graph.cytoscape_data(second_degree_sub),
        'third_degree': json_graph.cytoscape_data(third_degree_sub)
    }

    return JsonResponse(all_subgraphs)

