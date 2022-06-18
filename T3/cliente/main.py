"""
Módulo principal del cliente.
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from backend.cliente import Cliente
from utils import dato_json
from frontend.ventanaespera import VentanaEspera
from frontend.ventanainicio import VentanaInicio
from frontend.ventanajuego import VentanaJuego

if __name__ == "__main__":
    HOST = dato_json("host")
    PORT = dato_json("port")
    #RUTA_ICONO = os.path.join(*dato_json("RUTA_ICONO"))
    try:
        # =========> Instanciamos la APP <==========
        app = QApplication(sys.argv)
        # app.setWindowIcon(QIcon(RUTA_ICONO))
        # =========> Iniciamos el cliente <==========
        cliente = Cliente(HOST, PORT) # Backend
        ventana_juego = VentanaJuego() #Front
        ventana_inicio = VentanaInicio() #Front
        ventana_espera = VentanaEspera() #Front
        
        # =========> Conectamos señales entre el frontend y el back <==========
        ventana_inicio.senal_login.connect(cliente.enviar)
        ventana_inicio.senal_abrir_ventana_espera.connect(ventana_espera.mostrar_ventana)
        ventana_espera.senal_pedir_jugadores.connect(cliente.logica.pedir_jugadores)
        ventana_espera.senal_iniciar_juego.connect(cliente.logica.iniciar_juego)
        ventana_espera.senal_abrir_juego.connect(ventana_juego.mostrar_ventana)
        ventana_juego.senal_lanzar_dado.connect(cliente.logica.lanzar_dado)
        cliente.logica.senal_actualizar_ventana_espera.connect(ventana_espera.actualizar)
        cliente.logica.senal_nombre_de_usuario.connect(ventana_inicio.recibir_login)
        cliente.logica.senal_iniciar_juego.connect(ventana_espera.siguiente_ventana)
        cliente.logica.senal_numero_dado.connect(ventana_juego.resultado_dado)
        cliente.logica.senal_actualizar_tablero.connect(ventana_juego.actualizar_tablero)
        cliente.logica.senal_fin_del_juego.connect(ventana_juego.fin)
        # ========================================================================
        sys.exit(app.exec_())
    except ConnectionError as e:
        print("Ocurrió un error.", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente...")
        cliente.salir()
        sys.exit()