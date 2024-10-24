import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pickle

#uso este script para analizar la red


filename = "2024-10-08_unproyected.pkl"


def get_nodes_by_property(graph, property_name, value):
    return [n for n, attr in graph.nodes(data=True) if attr.get(property_name) == value]

def load_graph_pickle(filename):
    with open(filename, "rb") as f:
        graph = pickle.load(f)
    return graph
def find_first_matching_node(G, **attributes):
    for node, attrs in G.nodes(data=True):
        if all(attrs.get(key) == value for key, value in attributes.items()):
            return node
    return None
def find_node_with_highest_property(G, property_name):
    return max(G.nodes(data=True), key=lambda x: x[1].get(property_name, float('-inf')))[0]

red = load_graph_pickle(filename)
nodos_cubos = get_nodes_by_property(red, "object_type", "cube")  # lista de ids
nodos_cartas = get_nodes_by_property(red, "object_type", "card")

print("red entera: ",red)
print("cubos: ",len(nodos_cubos))
print("cartas: ",len(nodos_cartas))

#quiero una tablita con followers, numero de cubos
#busco maximo numero de followers
max_followers=float("-inf")
cubo_id_max_followers=""
for cubo_id in nodos_cubos:
    followers=len(red.nodes[cubo_id]["following"])
    if followers>max_followers:
        max_followers=followers
        cubo_id_max_followers=cubo_id
        print(max_followers,cubo_id_max_followers)
print("cubo con mas followers: ",cubo_id_max_followers)
print("tiene ",max_followers, " followers")


tablita=pd.DataFrame(columns=["N Followers","N Cubos"])
for i in range(0,max_followers+1):
    NCubos=len([n for n, attr in red.nodes(data=True) if attr.get("following") is not None and len(attr.get("following"))==i])
    observacion={"N Followers":i,"N Cubos":NCubos}
    tablita.loc[len(tablita)] = observacion
tablita.to_csv("followers.csv",index=False)

cubos_0_seguidores=[n for n, attr in red.nodes(data=True) if attr.get("following") is not None and len(attr.get("following"))==0]
print("cubos con 0 seguidores: ",len(cubos_0_seguidores))
cubos_1_seguidor=[n for n, attr in red.nodes(data=True) if attr.get("following") is not None and len(attr.get("following"))==1]
print("cubos con 1 seguidor: ",len(cubos_1_seguidor))
red.remove_nodes_from(cubos_0_seguidores)
print("red sin cubos con 0 seguidores: ", red)
red.remove_nodes_from(cubos_1_seguidor)
print("red con cubos con mas de 1 seguidor: ",red)

print("ejemplo cubo con 2 seguidores o mas: ",red.nodes[find_first_matching_node(red,object_type="cube")],"id: ",find_first_matching_node(red,object_type="cube"))
