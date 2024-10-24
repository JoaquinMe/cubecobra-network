import json
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pickle
import scipy.sparse as sp
from joblib import Parallel, delayed

#este script pasa de archivos json(cubos.json,oracle-cards.json, index.json) a un archivo .pkl
#que pueden levantar otros script

#NOTE:hacer que pase un archivo .pkl proyectado y otro no proyectado?


def get_nodes_by_property(graph, property_name, value):
    return [n for n, attr in graph.nodes(data=True) if attr.get(property_name) == value]


name = "2024-10-08"
with open(name + ".json", "r") as file:
    data_cubos = json.load(file)
with open("oracle-cards.json", "r") as file:
    data_cartas = json.load(file)
with open("indexToOracleMap.json", "r") as file:
    indice = json.load(file)
indice = {int(k): v for k, v in indice.items()}

# campos:
# cards
# id
# name
# owner
# owner_id
# image_uri
# image_artist
# card_count
# following

# hago dict de cubos
cubos_dict = {}
for cubo in data_cubos:
    cube_copy = {
        k if k != "iamge_artist" else "image_artist": v
        for k, v in cubo.items()
        if k != "id"
    }
    cube_copy["object_type"] = "cube"
    cubos_dict[cubo["id"]] = cube_copy

# hago dict de cartas
cartas_dict = {}
# checkear si quiero meter tcgplayer o cardmarket ids
fields_to_exclude = [
    "object",
    "id",
    "multiverse_ids",
    "mtgo_id",
    "mtgo_foil_id",
    "uri",
    "layout",
    "highres_image",
    "image_status",
    "image_uris",
    "games",
    "foil",
    "nonfoil",
    "oversized",
    "promo",
    "reprint",
    "variation",
    "set_name",
    "set_type",
    "set_uri",
    "set_search_uri",
    "scryfall_set_uri",
    "rulings_uri",
    "prints_search_uri",
    "digital",
    "card_back_id",
    "illustration_id",
    "border_color",
    "frame",
    "full_art",
    "textless",
    "story_spotlight",
    "related_uris",
    "purchase_uris",
]

for card in data_cartas:
    card_copy = {k: v for k, v in card.items() if k not in fields_to_exclude}
    card_copy["object_type"] = "card"
    cartas_dict[card["oracle_id"]] = card_copy

red = nx.Graph()
# Añado cada cubo con sus atributos
for node_id, attributes in cubos_dict.items():
    red.add_node(node_id, **attributes)

# Añado cada carta con sus atributos
for node_id, attributes in cartas_dict.items():
    red.add_node(node_id, **attributes)

nodos_cubos = get_nodes_by_property(red, "object_type", "cube")  # lista de ids
nodos_cartas = get_nodes_by_property(red, "object_type", "card")

i = 0
# enlazo
for cubo_id in nodos_cubos:
    cubo = red.nodes[cubo_id]
    cartas_en_el_cubo = cubo["cards"]

    cartas_indexadas = [indice[carta] for carta in cartas_en_el_cubo if carta != -1]
    # tengo que armar una lista de tuplas:
    enlaces = [(cubo_id, carta) for carta in cartas_indexadas]
    red.add_edges_from(enlaces)

with open(name + "_unproyected" + ".pkl", "wb") as f:
    pickle.dump(red, f)
