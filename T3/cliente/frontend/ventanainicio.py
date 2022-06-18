import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox)
from PyQt5.QtGui import QPixmap
from utils import dato_json
from PyQt5 import uic
from os.path import join

window_name, base_class = uic.loadUiType(join(*dato_json("ruta_ui_inicio")))



class VentanaInicio(window_name, base_class):

    senal_login = pyqtSignal(dict)
    senal_abrir_ventana_espera = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.boton.clicked.connect(self.enviar_datos)

    def ocultar(self):
        self.hide()

    def popup(self, texto):
        pop = QMessageBox()
        pop.setWindowTitle("Error")
        pop.setText(texto)
        pop.setIcon(QMessageBox.Critical)
        popup = pop.exec_()

    def enviar_datos(self):
        mensaje = {"comando": "login", "usuario": self.nombre_jugador.text()}
        self.senal_login.emit(mensaje)

    def recibir_login(self, respuesta):
        if respuesta == "vacio":
            self.popup("Por favor ingresa un nombre de usuario :(")
        if respuesta == "notalnum":
            self.popup("Tu nombre solo puede contener caracteres alfanumericos :(")
        elif respuesta == "over10":
            self.popup("Tu nombre es demasiado largo, este debe ser menor a 10 caracteres")
        elif respuesta == "True":
            self.hide()
            self.senal_abrir_ventana_espera.emit()
        elif respuesta == "roomisfull":
            self.popup("Lo siento la habitacion se lleno :(, juega mas tarde")


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaInicio()
    ventana.show()
    sys.exit(app.exec_())