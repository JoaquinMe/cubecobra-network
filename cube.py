#! /env/bin/python3
import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import lxml
import pickle


with open('test.json', 'r') as file:
    data_cubos = json.load(file)
with open('oracle-cards.json','r') as file:
    data_cartas=json.load(file)
with open('DBs/indexToOracleMap.json','r') as file:
    indice=json.load(file)
indice = {int(k): v for k, v in indice.items()}

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

#hago dict de cubos
cubos_dict = {
    
}
for cubo in data_cubos:
    cube_copy={k if k!='iamge_artist' else 'image_artist' :v for k,v in cubo.items() if k!= 'id'}
    cube_copy['object_type']="cube"
    cubos_dict[cubo['id']]=cube_copy

#print(cubos_dict["bffffb1a-2c70-4287-8e6d-cd080413577a"])

#hago dict de cartas
cartas_dict={}
                   #checkear si quiero meter tcgplayer o cardmarket ids                                                                       
fields_to_exclude=["object","id","multiverse_ids","mtgo_id","mtgo_foil_id",
                   "uri","layout","highres_image","image_status","image_uris",
                   "games","foil","nonfoil","oversized","promo","reprint",
                   "variation","set_name","set_type","set_uri","set_search_uri",
                   "scryfall_set_uri","rulings_uri","prints_search_uri","digital",
                   "card_back_id","illustration_id","border_color","frame",
                   "full_art","textless","story_spotlight","related_uris","purchase_uris"]

for card in data_cartas:
    card_copy={k: v for k, v in card.items() if k not in fields_to_exclude}
    card_copy['object_type'] = "card"
    cartas_dict[card['oracle_id']] = card_copy


def get_nodes_by_property(graph, property_name, value):
    return [n for n, attr in graph.nodes(data=True) if attr.get(property_name) == value]

red=nx.Graph()
#Añado cada cubo con sus atributos
for node_id, attributes in cubos_dict.items():
    red.add_node(node_id, **attributes)  

#Añado cada carta con sus atributos
for node_id, attributes in cartas_dict.items():
    red.add_node(node_id, **attributes)

nodos_cubos=get_nodes_by_property(red,"object_type","cube")
nodos_cartas=get_nodes_by_property(red,"object_type","card")

#hago enlaces
for nodo_id in nodos_cubos:
    for card in red.nodes[nodo_id]["cards"]:
        #tengo que linkear acá
        #print(card,nodo_id,"   ",indice[card])
        if(card in indice):
            red.add_edge(nodo_id,indice[card])

print(red)
with open("graph.pkl", "wb") as f:
    pickle.dump(red, f)
