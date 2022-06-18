"""
Módulo principal del servidor
"""
import sys
from servidor import Servidor
from utils import dato_json

if __name__ == "__main__":
    HOST = dato_json("host")
    PORT = dato_json("port")
    servidor = Servidor(HOST, PORT)

    try:
        while True:
            input("[Presione Ctrl+C para cerrar]".center(82, "+") + "\n")
    except KeyboardInterrupt:
        print("Cerrando servidor...".center(80, " "))
        sys.exit()
