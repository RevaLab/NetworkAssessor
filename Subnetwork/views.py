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