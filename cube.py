#! /env/bin/python3
import json
import pandas as pd
import networkx as nx

with open('DBs/cubes.json', 'r') as file:
    data = json.load(file)
#campos:
#cards
#id
#name
#owner
#owner_id
#image_uri
#image_artist
#card_count
#following

red=nx.Graph()
red_dict = {
    cube['id']: {k if k != 'iamge_artist' else 'image_artist': v for k, v in cube.items() if k != 'id'}
    for cube in data
}

red.add_nodes_from(red_dict.items())

#Hasta acá, cada nodo tiene todos los campos. No están conectados
print(red.nodes()["bffffb1a-2c70-4287-8e6d-cd080413577a"]["owner"])


