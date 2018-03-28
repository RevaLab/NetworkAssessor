import json
import pickle
import networkx as nx
from networkx.readwrite import json_graph

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .network_helpers import get_next_degree, get_pathway_counts


@csrf_exempt
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
    else:
        data = {}
    # load important pathways
    # pull out genes in selected pathways
    # create subnetwork with those genes + query genes
    # separate query genes and selected pathways
    query_genes = data['queryGenes']
    pathway_list = data['pathways']
    db = data['networkDatabase']

    # load databases
    interaction_db = pickle.load(open('static/{}.pkl'.format(db), 'rb'))
    pathways = pickle.load(open('static/important_pathways.pkl', 'rb'))
    node_list = list(query_genes)

    # add pathway genes to node list
    for pathway in pathway_list:
        if pathway == 'query-list':
            continue

        node_list += pathways[pathway]

    node_list = list(set(node_list))

    for pathway in pathways:
        per_pathway_node_list = node_list + pathways[pathway]
        per_pathway_subgraph = nx.Graph(interaction_db.subgraph(per_pathway_node_list))

        per_pathway_first_degree_sub = get_next_degree(query_genes, per_pathway_subgraph)

        print(pathway)
        print(len(per_pathway_first_degree_sub.edges()))
    # create subgraph from node list, including all pathway genes
    whole_subgraph = nx.Graph(interaction_db.subgraph(node_list))
    # get_pathway_counts(node_list, db)

    # get counts for all pathways for first degree
    # get_pathway_counts(node_list, db)

    # find next degree
    first_degree_sub = get_next_degree(query_genes, whole_subgraph)
    second_degree_sub = get_next_degree(first_degree_sub.nodes(), whole_subgraph)
    third_degree_sub = get_next_degree(second_degree_sub.nodes(), whole_subgraph)

    # subgraphs = [first_degree_sub, second_degree_sub, third_degree_sub]

    all_subgraphs = {
        'first_degree': first_degree_sub,
        'second_degree': second_degree_sub,
        'third_degree': third_degree_sub
    }

    all_json_graphs = {
        'first_degree': '',
        'second_degree': '',
        'third_degree': ''
    }

    for sub in all_subgraphs:
        json_sub = json_graph.node_link_data(all_subgraphs[sub])

        nodes_index = {}
        links_by_index = []

        for idx, node in enumerate(json_sub['nodes']):
            node_id = node['id']
            nodes_index[node_id] = idx
            if node_id in query_genes:
                if node_id in query_genes:
                    node['queryList'] = True
                else:
                    node['queryList'] = False

        for link in json_sub['links']:
            source = link['source']
            target = link['target']
            source_idx = nodes_index[source]
            target_idx = nodes_index[target]
            links_by_index.append(
                {'source': source_idx, 'target': target_idx}
            )
        json_sub['links'] = links_by_index

        all_json_graphs[sub] = json_sub

    return JsonResponse(all_json_graphs)

