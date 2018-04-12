import json
import pickle
import networkx as nx
from networkx.readwrite import json_graph

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .network_helpers import get_next_degree, normalize_user_pathways_by_gene, find_pathway_edge_count


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
    user_pathways = data['userPathways']
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

        try:
            node_list += pathways[pathway]
        except KeyError:
            node_list += user_pathways[pathway]['genes']

    node_list = list(set(node_list))

    pathways_edge_counts = {}

    # get counts for all pathways
    for pathway in pathways:
        per_pathway_node_list = node_list + pathways[pathway]
        pathway_edge_counts = find_pathway_edge_count(per_pathway_node_list, query_genes, interaction_db)
        pathways_edge_counts[pathway] = pathway_edge_counts

    # create subgraph from node list, including all pathway genes
    whole_subgraph = nx.Graph(interaction_db.subgraph(node_list))

    # add user pathways to subgraph nodes
    user_pathways_by_gene = normalize_user_pathways_by_gene(user_pathways)
    subgraph_pathways = nx.get_node_attributes(whole_subgraph, 'pathways')
    for gene in user_pathways_by_gene:
        if gene in subgraph_pathways:
            current_gene_pathways = subgraph_pathways[gene]
        else:
            current_gene_pathways = []

        if gene in node_list:
            current_gene_pathways += user_pathways_by_gene[gene]

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

    final_graphs = {
        'interaction_networks': all_json_graphs,
        'pathways_edge_counts': json.dumps(pathways_edge_counts)
    }

    return JsonResponse(final_graphs)

