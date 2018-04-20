import json
import _pickle as pickle
import networkx as nx

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .create_node_list import create_node_list
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

    previous_selected_pathways = data['previousSelectedPathways']
    current_pathway_edge_counts = data['pathwaysEdgeCounts']

    new_pathways = [pathway for pathway in pathway_list if pathway not in previous_selected_pathways]
    maintained_pathways = [pathway for pathway in pathway_list if pathway in previous_selected_pathways]

    # load databases
    interaction_db = nx.read_gpickle('static/{}.pkl'.format(db))
    db_pathways = pickle.load(open('static/important_pathways.pkl', 'rb'))

    node_list = create_node_list(query_genes, pathway_list, db_pathways, user_pathways)

    # Find nodes that are just in each pathway
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

    # Create whole_graph from node list,
    # which has genes from all selected
    # db_pathways + user_pathways
    whole_graph = nx.Graph(interaction_db.subgraph(node_list))

    # find degrees
    first_degree_sub = get_next_degree(query_genes, whole_graph)
    first_degree_nodes = list(first_degree_sub.nodes())
    print(first_degree_nodes)
    # if there are maintained pathways, include nodes only from those pathways
    # and ql as new center
    # maintained_pathway_ql_nodes = first_subgraph_nodes - all_new_pathway_only_nodes

    all_new_pathway_only_nodes = []
    all_new_pathway_nodes = []
    for pathway in new_pathways:
        try:
            all_new_pathway_only_nodes += nodes_just_from_each_pathway[pathway]
        except KeyError:
            pass
        try:
            all_new_pathway_nodes += db_pathways[pathway]
        except KeyError:
            all_new_pathway_nodes += user_pathways[pathway]['genes']

    maintained_pw_nodes_in_first_degree_nodes = []
    for pathway in maintained_pathways:
        maintained_pw_only_nodes = nodes_just_from_each_pathway[pathway]
        maintained_pw_nodes_in_first_degree_nodes += [node for node in maintained_pw_only_nodes if node in first_degree_nodes]
    first_degree_nodes_with_ql_and_maintained_pws = maintained_pw_nodes_in_first_degree_nodes + list(query_genes)

    if len(first_degree_nodes_with_ql_and_maintained_pws):
        # first_degree_nodes_with_ql_and_maintained_pws basically replaces the query list
        # all_new_pathway_only_nodes: whereas before, I added all the selected pathway nodes to the
        # subgraph, this time we're adding only the new pathway nodes
        new_node_list = first_degree_nodes_with_ql_and_maintained_pws + all_new_pathway_nodes
        new_whole_graph = nx.Graph(interaction_db.subgraph(new_node_list))

        first_degree_sub = get_next_degree(first_degree_nodes_with_ql_and_maintained_pws, new_whole_graph)
        first_degree_nodes = list(first_degree_sub.nodes())
        second_degree_sub = get_next_degree(first_degree_nodes + all_new_pathway_nodes, whole_graph)
        second_degree_nodes = list(second_degree_sub.nodes())
        third_degree_sub = get_next_degree(second_degree_nodes + all_new_pathway_nodes, whole_graph)
        third_degree_nodes = list(third_degree_sub.nodes())
    else:
        second_degree_sub = get_next_degree(first_degree_nodes, whole_graph)
        second_degree_nodes = list(second_degree_sub.nodes())
        third_degree_sub = get_next_degree(second_degree_nodes, whole_graph)
        third_degree_nodes = list(third_degree_sub.nodes())

    pathways_edge_counts = {}
    # get edge counts for all pathways
    for pathway in db_pathways:
        # For newly added pathways, we've already calculated the edges before selecting
        # so just report the previous edge count
        pw_nodes = db_pathways[pathway]
        if pathway in new_pathways:
            pathway_edge_counts = current_pathway_edge_counts[pathway]
            pathways_edge_counts[pathway] = pathway_edge_counts
            continue

        # For maintained pathways, recalculate the edges using the graph without
        # any of the pathway-exclusive nodes
        if pathway in maintained_pathways:
            # first_degree_nodes_wo_new_pw_nodes = []
            first_degree_nodes_wo_pw_nodes = [node for node in first_degree_nodes if node not in nodes_just_from_each_pathway[pathway]]
            second_degree_nodes_wo_pw_nodes = [node for node in second_degree_nodes if node not in nodes_just_from_each_pathway[pathway]]
            third_degree_nodes_wo_pw_nodes = [node for node in third_degree_nodes if node not in nodes_just_from_each_pathway[pathway]]
            pathway_edge_counts = {
                'first_degree': Parameter.edge_cross(pw_nodes, first_degree_nodes_wo_pw_nodes, interaction_db),
                'second_degree': Parameter.edge_cross(pw_nodes, second_degree_nodes_wo_pw_nodes, interaction_db),
                'third_degree': Parameter.edge_cross(pw_nodes, third_degree_nodes_wo_pw_nodes, interaction_db),
            }
            pathways_edge_counts[pathway] = pathway_edge_counts
            continue

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
        if pathway in new_pathways and pathway != 'query_list':
            pathway_edge_counts = current_pathway_edge_counts[pathway]
            pathways_edge_counts[pathway] = pathway_edge_counts
            continue

        if pathway in maintained_pathways:
            first_degree_nodes_wo_pw_nodes = [node for node in first_degree_nodes if
                                              node not in nodes_just_from_each_pathway[pathway]]
            second_degree_nodes_wo_pw_nodes = [node for node in second_degree_nodes if
                                               node not in nodes_just_from_each_pathway[pathway]]
            third_degree_nodes_wo_pw_nodes = [node for node in third_degree_nodes if
                                              node not in nodes_just_from_each_pathway[pathway]]
            pathway_edge_counts = {
                'first_degree': Parameter.edge_cross(pw_nodes, first_degree_nodes_wo_pw_nodes, interaction_db),
                'second_degree': Parameter.edge_cross(pw_nodes, second_degree_nodes_wo_pw_nodes, interaction_db),
                'third_degree': Parameter.edge_cross(pw_nodes, third_degree_nodes_wo_pw_nodes, interaction_db),
            }
            pathways_edge_counts[pathway] = pathway_edge_counts
            continue

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

