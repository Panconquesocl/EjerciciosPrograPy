"""
Modulo contiene funciones auxiliares
"""
import json
import os

def dato_json(llave):
    "Lee parametros.json y retorna el valor del dato"

    ruta_parametros = os.path.join("parametros.json")
    with open(ruta_parametros, "r", encoding="UTF-8") as archivo:
        diccionario_data = json.load(archivo)
    valor = diccionario_data[llave]
    return valor