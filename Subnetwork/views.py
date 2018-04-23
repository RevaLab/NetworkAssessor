import json
import _pickle as pickle
import networkx as nx

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .backend_plan import find_new_center, collect_all_nodes_for_subgraph, create_whole_graph_with_node_list
from .create_node_list import create_node_list
from .network_helpers import get_next_degree, normalize_user_pathways_by_gene
from .calculate_network_pathway_pval import calculate_network_pathway_pval
from networkx.readwrite import json_graph
from .network_utils import Parameter


@csrf_exempt
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
    else:
        data = {}

    # pull data from request
    query_genes = list(set(data['userPathways']['query_list']['genes']))
    user_pathways = data['userPathways']
    pathway_list = data['pathways'] # all selected pathways
    db = data['networkDatabase']

    previous_selected_pathways = data['previousSelectedPathways']
    current_pathway_edge_counts = data['pathwaysEdgeCounts']
    current_graph = data['currentGraph']

    maintained_pathways = [pathway for pathway in pathway_list if pathway in previous_selected_pathways]
    removed_pathways = [pathway for pathway in previous_selected_pathways if pathway not in pathway_list]

    # load databases
    interaction_db = nx.read_gpickle('static/{}.pkl'.format(db))
    db_pathways = pickle.load(open('static/important_pathways.pkl', 'rb'))

    # calculate graph
    all_nodes_for_subgraph = collect_all_nodes_for_subgraph(query_genes, pathway_list, db_pathways, user_pathways)
    whole_graph = create_whole_graph_with_node_list(interaction_db, all_nodes_for_subgraph)
    # node_list = create_node_list(query_genes, pathway_list, db_pathways, user_pathways)

    # Find nodes that are just in each pathway
    first_degree_sub = get_next_degree(query_genes, whole_graph)
    first_degree_nodes = list(first_degree_sub.nodes())
    second_degree_sub = get_next_degree(first_degree_nodes, whole_graph)
    second_degree_nodes = list(second_degree_sub.nodes())
    third_degree_sub = get_next_degree(second_degree_nodes, whole_graph)

    # get edge counts for all pathways
    pathways_edge_counts = {}
    all_pathways = list(user_pathways.keys()) + list(db_pathways.keys())
    for pathway in all_pathways:
        # For maintained pathways, keep the previously reported edge counts
        # since this is either the current edges or the previously anticipated connections
        if pathway in pathway_list and pathway != 'query_list':
            print(pathway)
            pathways_edge_counts[pathway] = current_pathway_edge_counts[pathway]
            continue

        if pathway in db_pathways:
            pw_nodes = db_pathways[pathway]
        else:
            pw_nodes = user_pathways[pathway]['genes']

        # For all other pathways, calculate the anticipated connections with the current subgraph
        # pathway_edge_counts = {
        #
        # }
        edges = Parameter.edge_cross(pw_nodes, query_genes, interaction_db)
        if edges:
            pathways_edge_counts[pathway] = edges
        else:
            pathways_edge_counts[pathway] = 0

    # get p values for db pathways
    # pathways_p_vals = {}
    #
    # for pathway in db_pathways:
    #     # For maintained pathways, keep the previously reported p values
    #     # if pathway in pathway_list:
    #
    #     pathway_p_vals = {
    #         'first_degree'
    #     }

    # add user pathways to graph nodes, which may already have pathways
    graph_pathways = nx.get_node_attributes(whole_graph, 'pathways')
    user_pathways_by_gene = normalize_user_pathways_by_gene(user_pathways)
    for gene in user_pathways_by_gene:
        if gene in graph_pathways:
            current_gene_pathways = graph_pathways[gene]
        else:
            current_gene_pathways = []

        if gene in all_nodes_for_subgraph:
            current_gene_pathways += user_pathways_by_gene[gene]

    subnetwork_and_edge_counts = {
        'subnetwork': {
            'first_degree': json_graph.cytoscape_data(first_degree_sub),
            'second_degree': json_graph.cytoscape_data(second_degree_sub),
            'third_degree': json_graph.cytoscape_data(third_degree_sub),
            'whole': json_graph.cytoscape_data(whole_graph)
        },
        'pathways_edge_counts': pathways_edge_counts,
    }

    return JsonResponse(subnetwork_and_edge_counts)

