import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pickle


filename = "2024-10-08_proyected.pkl"


def get_nodes_by_property(graph, property_name, value):
    return [n for n, attr in graph.nodes(data=True) if attr.get(property_name) == value]


def load_graph_pickle(filename):
    with open(filename, "rb") as f:
        graph = pickle.load(f)
    return graph


red = load_graph_pickle(filename)
print(red)
fuerzas_nodos = [data["strength"] for _, _, data in red.edges(data=True)]

plt.hist(fuerzas_nodos, color="skyblue", edgecolor="black", bins=30)
plt.xlabel("Fuerza de los enlaces")
plt.ylabel("Cantidad")
plt.title("Histograma de fuerza de enlace en la red")
plt.savefig(
    "edge_strength_histogram.png", format="png", dpi=300
)  # Saves as a high-resolution PNG
plt.close()  # Close the figure
