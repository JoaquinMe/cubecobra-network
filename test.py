
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


def jaccard(G, u, v):

    unbrs = set(G[u])

    vnbrs = set(G[v])

    return float(len(unbrs & vnbrs)) / len(unbrs | vnbrs)


red=nx.Graph()

red.add_nodes_from([1,2,3,4,5],bipartite=0)
red.add_nodes_from(["a","b","c","d"],bipartite=1)

edges=[(1,"a"),(1,"d"),(2,"c"),(3,"a"),(3,"b"),(4,"c"),(4,"d"),(5,"a"),(5,"d")]

red.add_edges_from(edges)

numeros=[n for n, attrs in red.nodes(data=True) if attrs.get("bipartite")==0]

pos = nx.bipartite_layout(red,numeros)

nx.draw(red, pos, with_labels=True, node_color='skyblue', node_size=800, font_size=12, font_weight='bold')

plt.show()

proyectada=nx.bipartite.generic_weighted_projected_graph(red,numeros,weight_function=jaccard)

pos_proyectada=nx.kamada_kawai_layout(proyectada)

nx.draw(proyectada,pos_proyectada,with_labels=True)

plt.show()

print(proyectada.edges(data=True))
