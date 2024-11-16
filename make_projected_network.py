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

cubos_a_borrar = [
    n for n, attr in red.nodes(data=True) if len(attr.get("following", [])) <= 1
]
print("antes de borrar: ", red)
red.remove_nodes_from(cubos_a_borrar)
print("dsps de borrar: ", red)
tamaño = red.number_of_nodes()
count = 0

print("antes de enlazar cubos", red)
# tiro enlaces entre todos los cubos
for nodo_i in red.nodes:
    for nodo_j in red.nodes:
        if nodo_i != nodo_j:
            fuerza = jaccard(red.nodes[nodo_i]["cards"], red.nodes[nodo_j]["cards"])

            if fuerza != 0:
                red.add_edge(nodo_i, nodo_j, strength=fuerza, edge_type="cube")
    count += 1
    print(
        f"progreso enlazado entre cubos: {(count / tamaño) * 100}%, {count} de {tamaño}",
        end="\r",
    )
print("despues de enlazar cubos", red)

lista_cubos = [
    n for n, attr in red.nodes(data=True) if attr.get("object_type", []) == "cube"
]

print("antes de poner users", red)
# añado users
for cubo_id in lista_cubos:
    dueño_id = red.nodes[cubo_id]["owner_id"]
    red.add_edge(cubo_id, dueño_id, edge_type="user")

    seguidores = red.nodes[cubo_id]["following"]
    seguidores = [
        seguidor for seguidor in seguidores if isinstance(seguidor, str)
    ]  # hay un cubo raro que tiene ids que no son str

    for seguidor in seguidores:
        red.add_node(seguidor, object_type="user")

    for seguidor in seguidores:
        red.add_edge(cubo_id, seguidor, edge_type="user")

print("despues de poner users", red)
with open(name + "_proyected" + ".pkl", "wb") as f:
    pickle.dump(red, f)
