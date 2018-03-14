import json
import pickle
import networkx as nx
from networkx.readwrite import json_graph

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request, gene_list):
    biogrid = pickle.load(open('static/biogrid.pkl', 'rb'))
    subgraph = biogrid.subgraph(gene_list.split('_n_'))
    json_sub = json_graph.node_link_data(subgraph)
    for node in json_sub['nodes']:
        node['queryList'] = True
    return JsonResponse(json_sub)


@csrf_exempt
def pathway_graph(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
    else:
        data = {}
    # load important pathways
    # pull out genes in selected pathways
    # create subnetwork with those genes + query genes
    print(data)
    # separate query genes and selected pathways
    query_genes = data['queryGenes']
    pathway_list = data['pathways']

    # load databases
    biogrid = pickle.load(open('static/biogrid.pkl', 'rb'))
    pathways = pickle.load(open('static/important_pathways.pkl', 'rb'))
    node_list = list(query_genes)

    # add pathway genes to node list
    for pathway in pathway_list:
        if pathway == 'query-list':
            continue

        node_list += pathways[pathway]

    node_list = list(set(node_list))

    # create subgraph from node list, including all pathway genes
    whole_subgraph = nx.Graph(biogrid.subgraph(node_list))

    query_list_neighbors = []

    for gene in query_genes:
        try:
            query_list_neighbors += whole_subgraph.neighbors(gene)
        except nx.exception.NetworkXError:
            pass

    # create subgraph from node list, including only pathway genes with a query gene neighbor
    first_degree_sub = nx.Graph(whole_subgraph.subgraph(query_list_neighbors + query_genes))
    first_degree_sub.remove_nodes_from(list(nx.isolates(first_degree_sub)))

    json_sub = json_graph.node_link_data(first_degree_sub)
    for node in json_sub['nodes']:
        if node['id'] in query_genes:
            node['queryList'] = 1
        else:
            node['queryList'] = 0

    return JsonResponse(json_sub)
