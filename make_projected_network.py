import json
import networkx as nx
import itertools
import pickle
from datasketch import MinHash

# NOTE:Tira enlaces con jaccard normal (no optimizado por tiempo)
# Tarda ~50 min en correr con ~6000 cubos en monocore
# Este script funciona bien y es un principio para hacer el análisis

# TODO: Hacer que corra paralelo.


# TODO: Chequear que funcione bien esta función
# Debería ser mas rapida que jaccard pero no está pasando eso
def minhash_jaccard(list1, list2, num_perm=64):
    m1, m2 = MinHash(num_perm=num_perm), MinHash(num_perm=num_perm)
    for item in list1:
        m1.update(str(item).encode("utf8"))
    for item in list2:
        m2.update(str(item).encode("utf8"))

    return m1.jaccard(m2)


def jaccard(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    # TODO:
    # chequear los casos borde y tirar return
    # devolver 0 si las listas no comparten nada. devolver 1 si las listas son iguales

    interseccion = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union != 0:
        return interseccion / union
    else:
        return 0


# Load data and build the initial graph
name = "2024-10-08"
with open(name + ".json", "r") as file:
    data_cubos = json.load(file)

cubos_dict = {}
for cubo in data_cubos:
    cube_copy = {
        k if k != "iamge_artist" else "image_artist": v
        for k, v in cubo.items()
        if k != "id"
    }
    cube_copy["object_type"] = "cube"
    cubos_dict[cubo["id"]] = cube_copy

red = nx.Graph()
for node_id, attributes in cubos_dict.items():
    red.add_node(node_id, **attributes)

cubos_pocos_seguidores = [
    n for n, attr in red.nodes(data=True) if len(attr.get("following")) <= 1
]
red.remove_nodes_from(cubos_pocos_seguidores)

cubos_vacios = [n for n, attr in red.nodes(data=True) if len(attr.get("cards")) == 0]
red.remove_nodes_from(cubos_vacios)

tamaño = red.number_of_nodes()
count = 0
print(red)
# tiro enlaces entre todos los cubos
for nodo_i in red.nodes:
    for nodo_j in red.nodes:
        if nodo_i != nodo_j:
            fuerza = jaccard(red.nodes[nodo_i]["cards"], red.nodes[nodo_j]["cards"])
            if fuerza != 0:
                red.add_edge(nodo_i, nodo_j, strength=fuerza)
    count += 1
    print(f"progreso: {(count / tamaño) * 100}%, {count} de {tamaño}", end="\r")
print(red)

with open(name + "_proyected+ " + ".pkl", "wb") as f:
    pickle.dump(red, f)
