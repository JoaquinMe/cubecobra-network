import json
import networkx as nx
import pickle
from datasketch import MinHash
from concurrent.futures import ProcessPoolExecutor, as_completed
import os


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
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union != 0:
        return intersection / union
    else:
        return 0


def compute_edges_for_node(node, nodes, graph_data):
    edges = []
    for other_node in nodes:
        if node != other_node:
            strength = jaccard(
                graph_data[node]["cards"], graph_data[other_node]["cards"]
            )
            if strength != 0:
                edges.append((node, other_node, strength))
    return edges


# Load data and build the initial graph
name = "2024-10-08"
with open(name + ".json", "r") as file:
    data_cubos = json.load(file)

cubos_dict = {
    cubo["id"]: {
        k if k != "iamge_artist" else "image_artist": v
        for k, v in cubo.items()
        if k != "id"
    }
    for cubo in data_cubos
}

red = nx.Graph()
for node_id, attributes in cubos_dict.items():
    red.add_node(node_id, **attributes)

cubos_pocos_seguidores = [
    n for n, attr in red.nodes(data=True) if len(attr.get("following")) <= 1
]
red.remove_nodes_from(cubos_pocos_seguidores)

cubos_vacios = [n for n, attr in red.nodes(data=True) if len(attr.get("cards")) == 0]
red.remove_nodes_from(cubos_vacios)

nodes = list(red.nodes)
graph_data = {n: red.nodes[n] for n in nodes}

# Parallel edge computation
num_perms = 64
with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
    futures = [
        executor.submit(compute_edges_for_node, node, nodes, graph_data)
        for node in nodes
    ]

    for future in as_completed(futures):
        edges = future.result()
        for node_i, node_j, strength in edges:
            red.add_edge(node_i, node_j, strength=strength)

print(red)

# Save the graph
with open(name + "_proyected_4CPUS.pkl", "wb") as f:
    pickle.dump(red, f)
