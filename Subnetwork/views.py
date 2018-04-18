import json
import _pickle as pickle
import networkx as nx

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

    query_genes = data['userPathways']['query_list']['genes']
    user_pathways = data['userPathways']
    pathway_list = data['pathways'] # all selected pathways
    db = data['networkDatabase']

    # load databases
    interaction_db = nx.read_gpickle('static/{}.pkl'.format(db))
    db_pathways = pickle.load(open('static/important_pathways.pkl', 'rb'))
    all_pw_dist = pickle.load(open('Pathway_distribution_sorted/all_pw_dist.pkl', 'rb'))
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

    # # find next degree
    first_degree_sub = get_next_degree(query_genes, whole_graph)
    first_degree_nodes = list(first_degree_sub.nodes())
    second_degree_sub = get_next_degree(first_degree_nodes, whole_graph)
    second_degree_nodes = list(second_degree_sub.nodes())
    third_degree_sub = get_next_degree(second_degree_nodes, whole_graph)
    # third_degree_nodes = third_degree_sub.nodes()

    pathways_edge_counts = {}
    pathways_network_p_vals = {}
    # get counts for all pathways
    for pathway in db_pathways:
        pw_nodes = list(db_pathways[pathway])
        # second_degree_pathway_node_list = first_degree_per_pathway_node_list + first_degree_nodes
        pathway_edge_counts = {
            'first_degree': Parameter.edge_cross(pw_nodes, first_degree_nodes, interaction_db),
            'second_degree': Parameter.edge_cross(pw_nodes, second_degree_nodes, interaction_db),
            'third_degree': 0 #Parameter.edge_cross(per_pathway_node_list, second_degree_nodes, interaction_db),
        }
        # per_pathway_node_list = node_list + db_pathways[pathway]
        pathways_edge_counts[pathway] = pathway_edge_counts
        # only calculate for pathway_network_p_val, as user pathways don't have distributions yet
        pathway_network_p_val = calculate_network_pathway_pval(node_list, db_pathways[pathway], pathway, interaction_db, all_pw_dist)
        pathways_network_p_vals[pathway] = pathway_network_p_val

    # for pathway in user_pathways:
    #     per_pathway_node_list = node_list + user_pathways[pathway]['genes']
    #     pathway_edge_counts = find_pathway_edge_count(per_pathway_node_list, query_genes, interaction_db)
    #     pathways_edge_counts[pathway] = pathway_edge_counts

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


    # get edge counts


    subnetwork_and_edge_counts = {
        'subnetwork': {
            'first_degree': json_graph.cytoscape_data(first_degree_sub),
            'second_degree': json_graph.cytoscape_data(second_degree_sub),
            'third_degree': json_graph.cytoscape_data(third_degree_sub)
        },
        'pathways_edge_counts': pathways_edge_counts,
        'pathways_network_p_vals': pathways_network_p_vals
    }

    return JsonResponse(subnetwork_and_edge_counts)

