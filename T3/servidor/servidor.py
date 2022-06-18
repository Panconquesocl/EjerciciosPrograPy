"""
Modulo contiene la implementación principal del servidor
"""
from matplotlib.font_manager import json_load
from logica import LogicaServidor
import socket
import threading
import json

class Servidor:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()
        self.logica = LogicaServidor(self)
        self.id_cliente = 0
        self.isonline = False
        self.clientes_conectados = []
        self.init_server()
        self.iniciar_conecciones()
        

    def init_server(self):
        self.socket_server.bind((self.host, self.port))
        self.isonline = True
        self.socket_server.listen()
        print(f"Servidor escuchando en {self.host}:{self.port}...")
        
    def iniciar_conecciones(self): #inicia un thread
        conecciones = threading.Thread(target= self.thread_establecer_conecciones)
        conecciones.start()

    def thread_establecer_conecciones(self): 
        # es un thread que esperara un cliente y generara otro thread para escuchar esta coneccion
        print("Servidor aceptando conexiones...")
        while True:
            try:
                socket_client, address = self.socket_server.accept()
                print("Conexión aceptada desde", address)
                self.clientes_conectados.append(socket_client)
                thread_comunicacion_cliente = threading.Thread(
                    target = self.thread_cliente,
                    args = (socket_client, ),
                    daemon = True)
                thread_comunicacion_cliente.start()
                #crear thread para cada cliente
            except ConnectionError:
                print("Ocurrio un error de coneccion")

    def thread_cliente(self, socket_cliente): # es un thread que intercambia info con un cliente
        print("Servidor conectado a un nuevo cliente...")
        self.recibir_datos(socket_cliente)

    def enviar(self, datos, socket_cliente): # envia mensajes 
        """
        Envía mensajes hacia algún socket cliente.

        """
        data = json.dumps(datos)
        bytes = data.encode()
        largo = len(bytes).to_bytes(4, byteorder='little')
        socket_cliente.sendall(largo + bytes)

    def codificar(self, info):
        pass


    def recibir_datos(self, socket_cliente): #
        while True:
            data = bytearray()
            bytes_largo = socket_cliente.recv(4)
            largo = int.from_bytes(bytes_largo, byteorder='little')
            while largo > len(data):
                lectura = min(4096, largo - len(data))
                data.extend(socket_cliente.recv(lectura))
            info_recibida = data.decode()
            info_recibida = json.loads(info_recibida)
            #self.echo(info_recibida, socket_cliente)# echo
            
            self.logica.procesar_info(info_recibida, socket_cliente)
