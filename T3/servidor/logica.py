"""
Modulo contiene la clase Logica del servidor
"""
from random import choice, randint
import threading


class Casilla:

    def __init__(self, id):
        self.id = str(id)
        self.color_adyacente = None
        self.siguiente = None
        self.siguiente_color = None
        self.final = False
        self.jugador_en_casilla = None
        self.casillas_restantes = None

    def __repr__(self):
        
        if self.siguiente != None: idsgte = self.siguiente.id 
        else: idsgte = "--" 
        string = f"La casilla {self.id} apunta a {idsgte} y {self.siguiente_color}"
        return string

class Tablero:

    def __init__(self, servidor):

        self.servidor = servidor

        self.tablero = []
        self.ruta_rosa = []
        self.ruta_beige = []
        self.ruta_verde = []
        self.ruta_celeste = []
        self.rutas = {
            "rosa": self.ruta_rosa, "beige": self.ruta_beige,
            "verde": self.ruta_verde, "celeste": self.ruta_celeste
                      }
        self.crear_ruta_especial("rosa")
        self.crear_ruta_especial("verde")
        self.crear_ruta_especial("beige")
        self.crear_ruta_especial("celeste")
        print(self.rutas)
        self.crear_tablero()

    def crear_ruta_especial(self, color):
        casilla_anterior = None
        for id in range(3):
            restante = 2 - id
            identificador = color + str(id)
            casilla = Casilla(identificador)
            casilla.casillas_restantes = restante
            self.rutas[color].append(casilla)
            if casilla_anterior is not None:
                casilla_anterior.siguiente = casilla
            casilla_anterior = casilla
            if id == 2: casilla.final = True

    def crear_tablero(self):
        casilla_anterior = None
        for id in range(16):
            casilla = Casilla(id)
            self.tablero.append(casilla)
            if casilla_anterior is not None: 
                casilla_anterior.siguiente = casilla
            if id == 3: 
                casilla.siguiente_color = self.ruta_beige[0]
                casilla.color_adyacente = "beige"
                casilla.casillas_restantes = 3
            elif id == 7: 
                casilla.siguiente_color = self.ruta_verde[0]
                casilla.color_adyacente = "verde"
                casilla.casillas_restantes = 3
            elif id == 11: 
                casilla.siguiente_color = self.ruta_rosa[0]
                casilla.color_adyacente = "rosa"
                casilla.casillas_restantes = 3
            elif id == 15:
                casilla.color_adyacente = "celeste" 
                casilla.siguiente = self.tablero[0]
                casilla.siguiente_color = self.ruta_celeste[0]
                casilla.casillas_restantes = 3
            casilla_anterior = casilla


class Jugador:

    def __init__(self, nombre, color, socket_cliente, tablero):
        self.color = color
        self.nombre = nombre
        self.socket_jugador = socket_cliente
        self.base = Casilla("base")
        self.pos_f1 = self.base
        self.pos_f2 = self.base
        self.dict_pos_fichas = {"f1": self.pos_f1, "f2": self.pos_f2}
        self.turno = 1
        self.fichas_base = 2
        self.fichas_color = 0
        self.fichas_victoria = 0
        self.is_turn = False
        self.tablero = tablero
        self.casilla_actual = None
        self.incolor = False

        if self.color == "celeste": self.base.siguiente = self.tablero.tablero[0]
        elif self.color == "beige": self.base.siguiente = self.tablero.tablero[4]
        elif self.color == "verde": self.base.siguiente = self.tablero.tablero[8]
        elif self.color == "rosa": self.base.siguiente = self.tablero.tablero[12] 

    def comido(self):
        if self.fichas_victoria == 1: self.pos_f2 = self.base
        elif self.fichas_victoria == 0: self.pos_f1 = self.base

    def resumen(self):
        pos_f1 = self.pos_f1
        pos_f2 = self.pos_f2
        if self.pos_f1 != "base": pos_f1 = self.pos_f1.id
        if self.pos_f2 != "base": pos_f2 = self.pos_f2.id 
        if self.pos_f1.final == True: pos_f1 = "win"
        if self.pos_f2.final == True: pos_f2 = "win"
        dict = {
            "nombre": self.nombre, "pos_f1": pos_f1, "pos_f2": pos_f2,
            "turno": self.turno, "fichas_base": self.fichas_base, "fichas_color": self.fichas_color,
            "fichas_victoria": self.fichas_victoria, "is_turn": self.is_turn 
                }
        return dict
    
    def avanzar(self, n):
        self.turno += 1
        print(self.color, "avanzara ", n, "espacios")
        if self.pos_f1.final == False: # checkear si la primera esta en base
            if self.incolor:
                print(n, self.pos_f1.casillas_restantes)
                if n == self.pos_f1.casillas_restantes:
                    self.incolor = False
                    self.pos_f1 == "win"
                    self.fichas_base = 1
                    self.fichas_victoria = 1
                    self.pos_f1 = self.pos_f1.siguiente
                else: pass
            else:      
                self.fichas_base = 1 
                casilla_actual = self.pos_f1
                for espacio in range(n):
                    if casilla_actual.color_adyacente == self.color: # Esta justo en el borde
                        print("debe entrar a zona color")
                        casilla_actual= casilla_actual.siguiente_color
                        self.incolor = True
                        self.fichas_color = 1
                        print(casilla_actual)
                    else: 
                        casilla_actual = casilla_actual.siguiente
                self.pos_f1.jugador_en_casilla = None 
                self.pos_f1 = casilla_actual
                self.check_casilla_ocupada(casilla_actual)
                self.pos_f1.jugador_en_casilla = self

        elif self.pos_f2.final == False: # check si la segunda aun no gana para mover esta
            if self.incolor:
                if n == self.pos_f2.casillas_restantes:
                    self.incolor = False
                    self.pos_f2 == "win"
                    self.fichas_base = 0
                    self.fichas_victoria = 2
                    print("jugador gano mandar senal a todos")
                    self.tablero.servidor.fin()
                else: pass
            else:        
                casilla_objetivo = self.pos_f2
                for espacio in range(n):
                    if casilla_objetivo.color_adyacente == self.color:
                        print("debe entrar a zona color")
                        self.incolor = True
                        self.fichas_color = 1
                        casilla_objetivo = casilla_objetivo.siguiente_color
                        print(casilla_objetivo)
                    else: 
                        casilla_objetivo = casilla_objetivo.siguiente
                self.fichas_base = 0
                self.pos_f2.jugador_en_casilla = None 
                self.pos_f2 = casilla_objetivo
                self.check_casilla_ocupada(casilla_objetivo)
                self.pos_f2.jugador_en_casilla = self     

        
    def check_casilla_ocupada(self, casilla):
        if casilla.final == True: pass
        else:
            if casilla.jugador_en_casilla is not None and casilla.jugador_en_casilla != self:
                casilla.jugador_en_casilla.comido()
                self.fichas_base += 1





class LogicaServidor:

    def __init__(self, parent):
        # Esto permite ejecutar funciones de la clase Servidor
        self.parent = parent
        self.dict_jugadores = dict()
        self.lista_jugadores = []
        self.colores_disponibles = ["rosa", "verde", "celeste", "beige"]
        self.colores =  ["rosa", "verde", "celeste", "beige"]
        self.cant_jugadores = 0
        self.tablero = Tablero(self)

    def procesar_info(self, info, socket_cliente):
        # Los lock solo estan aqui, ya que, todas las funciones son llamadas a partir de esta
        # es decir la logica procesara solo la info de un cliente a la vez
        self.parent.lock.acquire()
        print("Hola estoy procesando:", info)
        comando = info["comando"]
        if comando == "login":
            self.procesar_login(info, socket_cliente)

        elif comando == "pedirjugadores":
            self.enviar_jugadores_al_cliente(socket_cliente)

        elif comando == "start_game_request":
            self.iniciar_juego(socket_cliente)

        elif comando == "lanzar_dado":
            self.lanzar_dado(socket_cliente)
        else: 
            pass #mas comandos
        self.parent.lock.release()

    def enviar_jugadores_al_cliente(self, socket_cliente): # Seccion critica
        dict_info = dict()
        for sock_jugador in self.dict_jugadores:
            if sock_jugador == socket_cliente: 
                pass
            else:
                jugador = self.dict_jugadores[sock_jugador]
                dict_info[jugador.color] = jugador.nombre
        self.parent.enviar(
            {"comando": "jugadoresventanaespera", "log" : dict_info}, socket_cliente
                            )

    def procesar_login(self, info, socket_cliente): # Seccion critica
        nombre = info["usuario"]
        if nombre == "":
            self.parent.enviar({"comando": "login", "log": "vacio"}, socket_cliente)
        elif nombre.isalnum() == False:
            self.parent.enviar({"comando": "login", "log": "notalnum"}, socket_cliente)
        elif len(nombre) > 10:
            self.parent.enviar({"comando": "login", "log": "over10"}, socket_cliente)
        elif self.cant_jugadores == 4:
            self.parent.enviar({"comando": "login", "log": "roomisfull"}, socket_cliente)
        else:
            self.agregar_jugador(nombre, socket_cliente)

    def agregar_jugador(self, nombre, socket_jugador): # Seccion critica
        # Aqui no hay lock acquire ya que este ya se llamo en procesar login, solo se libera
        host = False
        if self.cant_jugadores == 0: host = True
        color_jugador = choice(self.colores_disponibles)
        self.colores_disponibles.remove(color_jugador)

        jugador = Jugador(nombre, color_jugador, socket_jugador, self.tablero)
        self.dict_jugadores[socket_jugador] = jugador
        self.lista_jugadores.append(jugador)
        
        self.parent.enviar(
            {"comando": "crearjugador",
             "log": {"color": color_jugador, "host": host, "nombre": nombre}}, socket_jugador
                           )
        self.parent.enviar({"comando": "login", "log": True}, socket_jugador)
        self.cant_jugadores += 1
        if self.cant_jugadores > 1:
            for sock_cliente in self.parent.clientes_conectados:
                self.enviar_jugadores_al_cliente(sock_cliente)
        if self.cant_jugadores == 4:
            self.iniciar_juego(socket_jugador)
            
    def iniciar_juego(self,socket_cliente):
        if self.cant_jugadores >= 2 and self.cant_jugadores <= 4:
            for cliente in self.parent.clientes_conectados:
                self.parent.enviar({"comando": "start_game", "log": "accepted"}, cliente)
            primer_jugador = self.lista_jugadores[0]
            primer_jugador.is_turn = True
            self.actualizar_tablero()
        else:
            self.parent.enviar({"comando": "start_game", "log": "denied"}, socket_cliente)

    def lanzar_dado(self, socket_cliente):
        jugador = self.dict_jugadores[socket_cliente]
        if jugador.is_turn:
            numero_obtenido = randint(1,3)
            jugador.avanzar(numero_obtenido)
            self.sendall({"comando": "resultado_dado", "log": numero_obtenido})
            jugador.is_turn = False
            self.actualizar_tablero()
            self.next_turn(jugador.color)
        self.actualizar_tablero()
        

    def next_turn(self, color_jugador_actual):
        check = False
        contador = 0
        for jugador in self.lista_jugadores:
            if check:
                jugador.is_turn = True
                break
            elif color_jugador_actual == jugador.color:
                if contador == (len(self.lista_jugadores) - 1):
                    self.lista_jugadores[0].is_turn = True
                    break
                else: check = True
            contador += 1


    def sendall(self, data):
        for cliente in self.parent.clientes_conectados:
            self.parent.enviar(data, cliente)

    def actualizar_tablero(self):
        logs = {}
        for socket_jugador in self.dict_jugadores:
            jugador = self.dict_jugadores[socket_jugador]
            dict_resumen = jugador.resumen()
            color = jugador.color
            logs[color] = dict_resumen
        self.sendall({"comando": "actualizar_tablero", "log": logs})

    def fin(self):
        logs = {}
        for socket_jugador in self.dict_jugadores:
            jugador = self.dict_jugadores[socket_jugador]
            dict_resumen = jugador.resumen()
            color = jugador.color
            logs[color] = dict_resumen
        self.sendall({"comando": "findeljuego", "log": logs})
        