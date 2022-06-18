import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtGui import QPixmap
from scipy.fft import ifftshift
from utils import dato_json
from PyQt5 import uic
from os.path import join

window_name, base_class = uic.loadUiType(join(*dato_json("ruta_ui_juego")))

class VentanaJuego(window_name, base_class):
    senal_lanzar_dado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.boton_dado.clicked.connect(self.lanzar_dado)
        self.boton_dado.hide()
        self.nombre = None
        self.pos_verde = None
        self.pos_beige = None
        self.pos_celeste = None
        self.pos_rosa = None
        self.tablero = {
            "0": self.cuadro0, "1": self.cuadro1, "2": self.cuadro2, "3": self.cuadro3,
            "4": self.cuadro4, "5": self.cuadro5, "6": self.cuadro6, "7": self.cuadro7,
            "8": self.cuadro8, "9": self.cuadro9, "10": self.cuadro10, "11": self.cuadro11,
            "12": self.cuadro12, "13": self.cuadro13, "14":self.cuadro14, "15": self.cuadro15,
            "rosa0": self.rosa0, "rosa1": self.rosa1, "rosa2": self.rosa2, "beige0": self.beige0,
            "beige1": self.beige1, "beige2": self.beige2, "celeste0": self.celeste0,
            "celeste1": self.celeste1, "celeste2": self.celeste2, "verde0": self.verde0,
            "verde1": self.verde1, "verde2": self.verde2
                        }

    def mostrar_ventana(self, nombre):
        self.nombre = nombre
        self.nombre_jugador.setText(self.nombre)
        self.show()

    def actualizar_tablero(self, dict_info):
        print(dict_info, "en ventana")
        if "verde" in dict_info:
            pixeles_ficha = QPixmap(join("Sprites", "Fichas", "Simples", "ficha-verde.png"))
            j_verde = dict_info["verde"]
            self.nombre_verde.setText(j_verde["nombre"])
            self.fichas_base_verde.setText("Fichas en base: " + str(j_verde["fichas_base"]))
            self.turno_verde.setText("Turno: " + str(j_verde["turno"]))
            self.fichas_encolor_verde.setText("Fichas en color: " + str(j_verde["fichas_color"]))
            self.fichas_victoria_verde.setText("Puntos:"  + str(j_verde["fichas_victoria"]))
            pos_f1 = j_verde["pos_f1"]
            pos_f2 = j_verde["pos_f2"]
            if self.pos_verde is not None: self.tablero[self.pos_verde].clear()
            if self.pos_rosa is not None: self.tablero[self.pos_rosa].clear()
            if self.pos_beige is not None: self.tablero[self.pos_beige].clear()
            if self.pos_celeste is not None: self.tablero[self.pos_celeste].clear()

            if pos_f1 == "base":
                pixeles = QPixmap(join("Sprites", "Fichas", "Dobles", "fichas-verdes.png"))
                self.base_verde.setPixmap(pixeles)
            else:   
                if pos_f1 != "win":
                    if self.pos_verde!= pos_f1 and self.pos_verde is not None: self.tablero[self.pos_verde].clear()
                    self.base_verde.setPixmap(pixeles_ficha)
                    self.tablero[pos_f1].setPixmap(pixeles_ficha)
                    self.pos_verde = pos_f1
                elif pos_f2 == "base":
                    self.base_verde.setPixmap(pixeles_ficha)
                    self.verde1.clear()
                    self.verde2.clear()
                elif pos_f2 != "win": 
                    if self.pos_verde != pos_f2 and self.pos_verde is not None: self.tablero[self.pos_verde].clear()
                    self.tablero[pos_f2].setPixmap(pixeles_ficha)
                    self.pos_verde = pos_f2
                else: 
                    self.verde1.clear()
                    self.verde2.clear()
                    
        if "celeste" in dict_info: 
            j_celeste = dict_info["celeste"]
            self.nombre_celeste.setText(j_celeste["nombre"])
            self.fichas_base_celeste.setText("Fichas en base: " + str(j_celeste["fichas_base"]))
            self.turno_celeste.setText("Turno: " + str(j_celeste["turno"]))
            self.fichas_encolor_celeste.setText("Fichas en color: " + str(j_celeste["fichas_color"]))
            self.fichas_victoria_celeste.setText("Puntos:"  + str(j_celeste["fichas_victoria"]))
            pixeles_ficha = QPixmap(join("Sprites", "Fichas", "Simples", "ficha-azul.png"))
            pos_f1 = j_celeste["pos_f1"]
            pos_f2 = j_celeste["pos_f2"]

            if pos_f1 == "base":
                pixeles = QPixmap(join("Sprites", "Fichas", "Dobles", "fichas-azules.png"))
                self.base_celeste.setPixmap(pixeles)
            else:    
                if pos_f1 != "win":
                    if self.pos_celeste != pos_f1 and self.pos_celeste is not None: self.tablero[self.pos_celeste].clear() 
                    self.base_celeste.setPixmap(pixeles_ficha)
                    self.tablero[pos_f1].setPixmap(pixeles_ficha)
                    self.pos_celeste = pos_f1
                elif pos_f2 == "base":
                    self.base_celeste.setPixmap(pixeles_ficha)
                    self.celeste1.clear()
                    self.celeste2.clear()
                elif pos_f2 != "win": 
                    if self.pos_celeste != pos_f2 and self.pos_celeste is not None: self.tablero[self.pos_celeste].clear() 
                    self.tablero[pos_f2].setPixmap(pixeles_ficha)
                    self.pos_celeste = pos_f2
                else: 
                    self.celeste1.clear()
                    self.celeste2.clear()

        if "beige" in dict_info:
            j_beige = dict_info["beige"]
            self.nombre_beige.setText(j_beige["nombre"])
            self.fichas_base_beige.setText("Fichas en base: " + str(j_beige["fichas_base"]))
            self.turno_beige.setText("Turno: " + str(j_beige["turno"]))
            self.fichas_encolor_beige.setText("Fichas en color: " + str(j_beige["fichas_color"]))
            self.fichas_victoria_beige.setText("Puntos:"  + str(j_beige["fichas_victoria"]))
            pos_f1 = j_beige["pos_f1"]
            pos_f2 = j_beige["pos_f2"]
            pixeles_ficha = QPixmap(join("Sprites", "Fichas", "Simples", "ficha-amarilla.png"))


            if pos_f1 == "base":
                pixeles = QPixmap(join("Sprites", "Fichas", "Dobles", "fichas-amarillas.png"))
                self.base_beige.setPixmap(pixeles)
            else:    
                if pos_f1 != "win":
                    if self.pos_beige != pos_f1 and self.pos_beige is not None: self.tablero[self.pos_beige].clear()
                    self.base_beige.setPixmap(pixeles_ficha)
                    self.tablero[pos_f1].setPixmap(pixeles_ficha)
                    self.pos_beige = pos_f1
                elif pos_f2 == "base":
                    self.base_beige.setPixmap(pixeles_ficha)
                    self.beige1.clear()
                    self.beige2.clear()
                elif pos_f2 != "win": 
                    if self.pos_beige != pos_f2 and self.pos_beige is not None: self.tablero[self.pos_beige].clear()
                    self.tablero[pos_f2].setPixmap(pixeles_ficha)
                    self.pos_beige = pos_f2
                else: 
                    self.beige1.clear()
                    self.beige2.clear()

        if "rosa" in dict_info:
            j_rosa = dict_info["rosa"]
            self.nombre_rosa.setText(j_rosa["nombre"])
            self.fichas_base_rosa.setText("Fichas en base: " + str(j_rosa["fichas_base"]))
            self.turno_rosa.setText("Turno: " + str(j_rosa["turno"]))
            self.fichas_encolor_rosa.setText("Fichas en color: " + str(j_rosa["fichas_color"]))
            self.fichas_victoria_rosa.setText("Puntos:"  + str(j_rosa["fichas_victoria"]))
            pixeles_ficha = QPixmap(join("Sprites", "Fichas", "Simples", "ficha-roja.png"))
            pos_f1 = j_rosa["pos_f1"]
            pos_f2 = j_rosa["pos_f2"]

            if pos_f1 == "base":
                pixeles = QPixmap(join("Sprites", "Fichas", "Dobles", "fichas-rojas.png"))
                self.base_rosa.setPixmap(pixeles)
            else:    
                if pos_f1 != "win":
                    if self.pos_rosa != pos_f1 and self.pos_rosa is not None: self.tablero[self.pos_rosa].clear()
                    self.base_rosa.setPixmap(pixeles_ficha)
                    self.tablero[pos_f1].setPixmap(pixeles_ficha)
                    self.pos_rosa = pos_f1
                elif pos_f2 == "base":
                    self.base_rosa.setPixmap(pixeles_ficha)
                    self.rosa1.clear()
                    self.rosa2.clear()
                elif pos_f2 != "win": 
                    if self.pos_beige != pos_f2 and self.pos_beige is not None: self.tablero[self.pos_beige].clear()
                    self.tablero[pos_f2].setPixmap(pixeles_ficha)
                    self.pos_beige = pos_f2
                else: 
                    self.rosa1.clear()
                    self.rosa2.clear()

        for key_jugador in dict_info:
            jugador = dict_info[key_jugador]
            if jugador["is_turn"] == True: 
                self.jugador_de_turno.setText(jugador["nombre"])
                if jugador["nombre"] == self.nombre: self.boton_dado.show()
            
    def lanzar_dado(self):
        self.senal_lanzar_dado.emit()

    def resultado_dado(self, numero):
        self.boton_dado.hide()
        self.numero_obtenido.setText(str(numero))

    def fin(self):
        self.hide()

if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaJuego()
    ventana.show()
    sys.exit(app.exec_())