import json
import _pickle as pickle
import networkx as nx

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .backend_plan import find_new_center, collect_all_nodes_for_subgraph, create_whole_graph_with_node_list, \
    delete_removed_pathway_nodes_from_center
from .create_node_list import create_node_list
from .find_nodes_unique_to_pathways import find_nodes_unique_to_pathways
from .network_helpers import get_next_degree, normalize_user_pathways_by_gene, find_pathway_edge_count
from .calculate_network_pathway_pval import calculate_network_pathway_pval
from networkx.readwrite import json_graph
from .network_utils import Parameter

@csrf_exempt
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
    else:
        data = {}

    query_genes = list(set(data['userPathways']['query_list']['genes']))
    user_pathways = data['userPathways']
    pathway_list = data['pathways'] # all selected pathways
    db = data['networkDatabase']

    previous_selected_pathways = data['previousSelectedPathways']
    current_pathway_edge_counts = data['pathwaysEdgeCounts']
    current_graph = data['currentGraph']

    new_pathways = [pathway for pathway in pathway_list if pathway not in previous_selected_pathways]
    maintained_pathways = [pathway for pathway in pathway_list if pathway in previous_selected_pathways]
    removed_pathways = [pathway for pathway in previous_selected_pathways if pathway not in pathway_list]

    # load databases
    interaction_db = nx.read_gpickle('static/{}.pkl'.format(db))
    db_pathways = pickle.load(open('static/important_pathways.pkl', 'rb'))

    center = find_new_center(query_genes, current_graph, 'first_degree', removed_pathways, maintained_pathways,
                             db_pathways, user_pathways)
    all_nodes_for_subgraph = collect_all_nodes_for_subgraph(center, new_pathways, db_pathways, user_pathways)
    whole_graph = create_whole_graph_with_node_list(interaction_db, all_nodes_for_subgraph)

    node_list = create_node_list(query_genes, pathway_list, db_pathways, user_pathways)

    # Find nodes that are just in each pathway
    nodes_just_from_each_pathway = find_nodes_unique_to_pathways(node_list, pathway_list, db_pathways, user_pathways)
    first_degree_sub = get_next_degree(center, whole_graph, 'first')
    first_degree_nodes = list(first_degree_sub.nodes())
    second_degree_sub = get_next_degree(first_degree_nodes, whole_graph, 'second')
    second_degree_nodes = list(second_degree_sub.nodes())
    third_degree_sub = get_next_degree(second_degree_nodes, whole_graph, 'third')
    third_degree_nodes = list(third_degree_sub.nodes())

    pathways_edge_counts = {}
    # get edge counts for all pathways
    for pathway in db_pathways:
        # For newly added pathways, we've already calculated the edges before selecting
        # so just report the previous edge count
        pw_nodes = db_pathways[pathway]
        pathway_edge_counts = {
            'first_degree': Parameter.edge_cross(pw_nodes, first_degree_nodes, interaction_db),
            'second_degree': Parameter.edge_cross(pw_nodes, second_degree_nodes, interaction_db),
            'third_degree': Parameter.edge_cross(pw_nodes, third_degree_nodes, interaction_db),
        }
        pathways_edge_counts[pathway] = pathway_edge_counts
        # # only calculate for pathway_network_p_val, as user pathways don't have distributions yet
        # pathway_network_p_val = calculate_network_pathway_pval(node_list, db_pathways[pathway], pathway, interaction_db, all_pw_dist)
        # pathways_network_p_vals[pathway] = pathway_network_p_val

    for pathway in user_pathways:
        pw_nodes = list(user_pathways[pathway]['genes'])
        pathway_edge_counts = {
            'first_degree': Parameter.edge_cross(pw_nodes, first_degree_nodes, interaction_db),
            'second_degree': Parameter.edge_cross(pw_nodes, second_degree_nodes, interaction_db),
            'third_degree': Parameter.edge_cross(pw_nodes, third_degree_nodes, interaction_db),
        }
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

    subnetwork_and_edge_counts = {
        'subnetwork': {
            'first_degree': json_graph.cytoscape_data(first_degree_sub),
            'second_degree': json_graph.cytoscape_data(second_degree_sub),
            'third_degree': json_graph.cytoscape_data(third_degree_sub)
        },
        'pathways_edge_counts': pathways_edge_counts,
        # 'pathways_network_p_vals': pathways_network_p_vals
    }

    return JsonResponse(subnetwork_and_edge_counts)

