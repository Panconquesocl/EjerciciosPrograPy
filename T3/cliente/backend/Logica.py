from PyQt5.QtCore import pyqtSignal, QObject
import random


class Jugador():

    def __init__(self):
        self.color = None
        self.nombre = None
        self.ishost = None

class Logica(QObject, Jugador):
    senal_nombre_de_usuario = pyqtSignal(str)
    senal_actualizar_ventana_espera = pyqtSignal(dict)
    senal_iniciar_juego = pyqtSignal(bool)
    senal_numero_dado = pyqtSignal(int)
    senal_actualizar_tablero = pyqtSignal(dict)
    senal_fin_del_juego = pyqtSignal()

    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        
    def procesar_info(self, info):
        ("Hola estoy procesando:", info)
        comando = info["comando"]
        log = info["log"]
        if comando == "login":
            if log == "vacio":
                self.senal_nombre_de_usuario.emit("vacio")
            elif log == "notalnum":
                self.senal_nombre_de_usuario.emit("notalnum")
            elif log == "over10":
                self.senal_nombre_de_usuario.emit("over10")
            elif log == True:
                self.senal_nombre_de_usuario.emit("True")
            elif log == "roomisfull":
                self.senal_nombre_de_usuario.emit("roomisfull")
            else: print("algo raro ha ocurrido")

        elif comando == "crearjugador":
            self.color = log["color"]
            self.host = log["host"]
            self.nombre = log["nombre"]
            info_client = {"comando": "jugador", "log": {"nombre": self.nombre, "color": self.color, "host": self.host}}
            self.senal_actualizar_ventana_espera.emit(info_client)

        elif comando == "jugadoresventanaespera":
            jugadores = {"comando": "jugadores","log": log }
            self.senal_actualizar_ventana_espera.emit(jugadores)

        elif comando == "start_game":
            if log == "accepted":
                self.senal_iniciar_juego.emit(True)
            elif log == "denied":
                self.senal_iniciar_juego.emit(False)
        elif comando == "resultado_dado":
            self.senal_numero_dado.emit(log)
        elif comando == "actualizar_tablero":
            self.senal_actualizar_tablero.emit(log)
        elif comando == "findeljuego":
            self.senal_fin_del_juego.emit()
            
    def pedir_jugadores(self):
        dato = {"comando": "pedirjugadores"}
        self.parent.enviar(dato)

    def iniciar_juego(self):
        self.parent.enviar({"comando": "start_game_request"})

    def lanzar_dado(self):
        self.parent.enviar({"comando":"lanzar_dado"})
