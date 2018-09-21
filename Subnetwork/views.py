import datetime
import json
import _pickle as pickle
import networkx as nx

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .network_functions import \
    collect_all_nodes_for_subgraph, \
    make_three_degrees_of_graphs, \
    calculate_pathway_edge_counts, \
    assign_user_pathways_to_genes
from .calculate_network_pathway_pval import calculate_all_pathways_p_vals
from .calculate_internal_p_val import calculate_internal_p_val


@csrf_exempt
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
    else:
        data = {}

    # pull data from request
    query_genes = list(set(data['userPathways']['query_list']['genes']))
    len_query_gene_set = len(query_genes)
    user_pathways = data['userPathways']
    pathway_list = data['pathways']  # all selected pathways
    db = data['networkDatabase']

    # load databases
    # interaction_db = nx.read_gpickle('static/{}_with_pathways.pkl'.format(db))
    interaction_db = nx.read_gpickle('static/{}_with_relations.pkl'.format(db))
    pathway_neighbors = pickle.load(open('static/pathway_neighbors_{}.pkl'.format(db), 'rb'))
    db_pathways = pickle.load(open('static/important_pathways.pkl', 'rb'))
    all_gene_set_pathway_p_vals = pickle.load(open('static/p_vals_per_gene_count_per_edge_count_biogrid.pkl', 'rb'))
    db_distribution = pickle.load(open('static/{}_dist.pkl'.format(db), 'rb'))

    # calculate graphs
    all_nodes_for_subgraph = collect_all_nodes_for_subgraph(query_genes, pathway_list, db_pathways, user_pathways)
    whole_graph = nx.Graph(interaction_db.subgraph(all_nodes_for_subgraph))
    subnetworks = make_three_degrees_of_graphs(query_genes, whole_graph)

    # calculate internal p val
    # internal_p_val = calculate_internal_p_val(query_genes, interaction_db, db_distribution)
    internal_p_val = 0

    # get edge counts for all pathways and calculate p vals
    pathways_edge_counts = calculate_pathway_edge_counts(query_genes, db_pathways, pathway_neighbors)
    pathways_p_vals = calculate_all_pathways_p_vals(pathways_edge_counts, len_query_gene_set, all_gene_set_pathway_p_vals)

    # add user pathways to graph nodes, which may already have pathways
    assign_user_pathways_to_genes(user_pathways, whole_graph, all_nodes_for_subgraph)

    subnetwork_and_edge_counts = {
        'subnetwork': subnetworks,
        'pathways_edge_counts': pathways_edge_counts,
        'pathways_p_vals': pathways_p_vals,
        'internal_p_val': internal_p_val
    }

    return JsonResponse(subnetwork_and_edge_counts)



@csrf_exempt
def bug_report(request):
    data = json.loads(request.body.decode('utf-8'))
    bug_report = data['bugReport']

    today = datetime.date.today()
    bug_report_file = 'bug_reports/{}.txt'.format(today)
    with open(bug_report_file, 'a+') as f:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(time)
        f.write("\n")
        for el in bug_report:
            if len(bug_report[el]):
                f.write(el)
                f.write("\n")
                f.write(bug_report[el])
            f.write("\n")
        f.write("*****************************")
        f.write("\n")

    return HttpResponse(status=200)

