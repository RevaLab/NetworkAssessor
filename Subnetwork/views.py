import pickle
import networkx as nx
from networkx.readwrite import json_graph

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


# Create your views here.
def index(request, gene_list):
    biogrid = pickle.load(open('static/biogrid.pkl', 'rb'))
    subgraph = biogrid.subgraph(gene_list.split('_n_'))
    json_sub = json_graph.node_link_data(subgraph)
    for node in json_sub['nodes']:
        node['queryList'] = True
    return JsonResponse(json_sub)


def pathway_graph(request, query_genes_pw_data):
    # load important pathways
    # pull out genes in selected pathways
    # create subnetwork with those genes + query genes

    # separate query genes and selected pathways
    data = query_genes_pw_data.split('_t_')
    query_genes = data[0].split('_n_')
    pathway_list = data[1].split('_n_')

    # load databases
    biogrid = pickle.load(open('static/biogrid.pkl', 'rb'))
    pathways = pickle.load(open('static/important_pathways.pkl', 'rb'))
    node_list = query_genes

    # add pathway genes to node list
    for pathway in pathway_list:
        node_list += pathways[pathway]
    node_list = list(set(node_list))

    # create subgraph from node list
    subgraph = biogrid.subgraph(node_list)
    json_sub = json_graph.node_link_data(subgraph)
    for node in json_sub['nodes']:
        if node in query_genes:
            node['queryList'] = True
        else:
            node['queryList'] = False
    return JsonResponse(json_sub)
