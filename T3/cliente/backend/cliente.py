import socket
from backend.Logica import Logica
import threading
import json

class Cliente:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logica = Logica(self)
        self.init_cliente()

    def init_cliente(self): #listo
        try:
            self.socket_cliente.connect((self.host, self.port))
            self.start_listening()
            print("Conneccion exitosa")
            
        except ConnectionError:
            print("Ocurrio un error de coneccion")

    def start_listening(self): #listo
        thread_escuchar_servidor = threading.Thread(target= self.thread_escuchar, daemon=True)
        thread_escuchar_servidor.start()

    def thread_escuchar(self): #listo
        self.recibir()
            
    def enviar(self, data):
        data = json.dumps(data)
        bytes = data.encode()
        largo = len(bytes).to_bytes(4, byteorder='little')
        self.socket_cliente.sendall(largo + bytes)

    def recibir(self):
        while True:
            data = bytearray()
            bytes_largo = self.socket_cliente.recv(4)
            largo = int.from_bytes(bytes_largo, byteorder='little')
            while largo > len(data):
                lectura = min(4096, largo - len(data))
                data.extend(self.socket_cliente.recv(lectura))
            info_recibida = data.decode()
            info_recibida = json.loads(info_recibida)
            self.logica.procesar_info(info_recibida)
            

    def encriptar(self):
        pass

    def codificar(self):
        pass





    
