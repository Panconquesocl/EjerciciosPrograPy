import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox)
from PyQt5.QtGui import QPixmap
from utils import dato_json
from PyQt5 import uic
from os.path import join

window_name, base_class = uic.loadUiType(join(*dato_json("ruta_ui_espera")))

class VentanaEspera(window_name, base_class):

    senal_pedir_jugadores = pyqtSignal()
    senal_iniciar_juego = pyqtSignal()
    senal_abrir_juego = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.boton.hide()
        self.lista_espacios = [self.nombre_jugador_2, self.nombre_jugador_3, self.nombre_jugador_4]
        self.lista_imagenes = [self.img_ficha_2, self.img_ficha_3, self.img_ficha_4]
        self.dict_rutas = {"rosa": join("Sprites", "Fichas", "Simples", "ficha-roja.png"),"verde": join("Sprites", "Fichas", "Simples", "ficha-verde.png"),"celeste": join("Sprites", "Fichas", "Simples", "ficha-azul.png"),"beige": join("Sprites", "Fichas", "Simples", "ficha-amarilla.png")}
        self.boton.clicked.connect(self.iniciar_juego)
        self.nombre_j = None

    def iniciar_juego(self):
        print("click")
        self.senal_iniciar_juego.emit()

    def mostrar_ventana(self):
        self.pedir_datos_jugadores()
        self.show()

    def pedir_datos_jugadores(self):
        self.senal_pedir_jugadores.emit()

    def popup(self, texto):
        pop = QMessageBox()
        pop.setWindowTitle("Error")
        pop.setText(texto)
        pop.setIcon(QMessageBox.Critical)
        popup = pop.exec_()

    def actualizar(self, data):
        print("Actualizando venta de espera.......")
        if data["comando"] == "jugador":
            datos = data["log"]
            nombre = datos["nombre"]
            self.nombre_j = nombre
            color = datos["color"]
            print("Actualizando Jugador........", datos)
            self.nombre_jugador.setText(f"{nombre}               {color}")
            if datos["host"] == True: self.boton.show()
            pixeles = QPixmap(self.dict_rutas[color])
            self.img_ficha.setPixmap(pixeles)

        elif data["comando"] == "jugadores":
            datos = data["log"]
            contador = 0
            print("actualizando jugadores.......", datos)
            for color in datos:
                nombre_jugador = datos[color]
                self.lista_espacios[contador].setText(f"{nombre_jugador}               {color}")
                pixeles = QPixmap(self.dict_rutas[color])
                self.lista_imagenes[contador].setPixmap(pixeles)
                contador += 1

    def siguiente_ventana(self, bool):
        if bool: 
            self.hide()
            self.senal_abrir_juego.emit(self.nombre_j)
        else: self.popup("Aun no puedes empezar el juego")


    

if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaEspera()
    ventana.show()
    sys.exit(app.exec_())