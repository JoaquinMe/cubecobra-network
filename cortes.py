# este script levanta la red original pesada
# y  serialmente va cortando enlaces por peso y los va guardando
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pickle
import os

filename = "2024-10-08_proyected.pkl"


def get_nodes_by_property(graph, property_name, value):
    return [n for n, attr in graph.nodes(data=True) if attr.get(property_name) == value]


def load_graph_pickle(filename):
    with open(filename, "rb") as f:
        graph = pickle.load(f)
    return graph


def cortar(red_, corte):
    lista_enlaces_a_cortar = []
    for enlace in red_.edges(data=True):
        cubo_i = enlace[0]
        cubo_j = enlace[1]
        atributos = enlace[2]
        if atributos["edge_type"] == "cube":
            if atributos["strength"] <= corte:
                lista_enlaces_a_cortar.append((cubo_i, cubo_j))
    red_.remove_edges_from(lista_enlaces_a_cortar)
    return red_


red = load_graph_pickle(filename)
print(red)
secuencia = np.arange(0, 1, 0.01)
red_original = red.copy()

for v in secuencia:
    cortar(red, v)
    print(red, v)
    with open(
        os.path.join("cortes", "corte_red_proyectada_" + str(v) + ".pkl"), "wb"
    ) as f:
        pickle.dump(red, f)
