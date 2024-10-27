import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

name = "2024-10-08"
with open(name + ".json", "r") as file:
    data_cubos = json.load(file)


def give_count_between_ns(bot, top, lista):
    i = 0
    for item in lista:
        if bot <= item <= top:
            i += 1
    return i


cubos_dict = {}
for cubo in data_cubos:
    cube_copy = {
        k if k != "iamge_artist" else "image_artist": v
        for k, v in cubo.items()
        if k != "id"
    }
    cube_copy["object_type"] = "cube"
    cubos_dict[cubo["id"]] = cube_copy

lista_cant_cartas_1 = []

for cubo_id in cubos_dict:
    lista_cant_cartas_1.append(len(cubos_dict[cubo_id]["cards"]))


data_raw = pd.Series(lista_cant_cartas_1, name="N Cartas")
print(data_raw.describe())

# hacer histograma
plt.hist(lista_cant_cartas_1)
plt.show()

# opero sobre los cubos que tienen mas de dos seguidores
lista_cant_cartas_2 = []
for cubo_id in cubos_dict:
    if len(cubos_dict[cubo_id]["following"]) >= 2:
        lista_cant_cartas_2.append(len(cubos_dict[cubo_id]["cards"]))

data_curada = pd.Series(lista_cant_cartas_2, name="N Cartas")
print(data_curada.describe())
plt.hist(lista_cant_cartas_2)
plt.show()
