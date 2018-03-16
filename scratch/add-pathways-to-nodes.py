import pickle
import networkx as nx

# load database

hprd = pickle.load(open('scratch/hprd_simple.pkl', 'rb'))

# make into graph
g = nx.Graph()
g.add_nodes_from(hprd.keys())

for k, v in hprd.items():
    g.add_edges_from(([(k, t) for t in v]))

# load pathways by gene

pathways_by_gene = pickle.load(open('static/important_pathways_by_gene.pkl', 'rb'))

nx.set_node_attributes(g, values=pathways_by_gene, name='pathways')

# put into pickle
with open('static/hprd.pkl', 'wb') as f:
    pickle.dump(g, f)