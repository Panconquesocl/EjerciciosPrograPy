class TorreDeHanoi:
    
    def __init__(self):
        self.pilar_1 = [6, 5, 4, 3, 2, 1]
        self.pilar_2 = []
        self.pilar_3 = []

    def Mover_disco(self, pilar_origen, pilar_destino):
        self.origen = pilar_origen # Toma valores entre 1 - 3
        self.destino = pilar_destino
        pilares = {1 : self.pilar_1, 2 : self.pilar_2, 3 : self.pilar_3}
        # Verificar si existe un disco
        if pilares[self.origen] == []:
            print("No hay Disco")
        else: 
            # Verificar si el movimiento es valido
            if pilares[self.destino] == []:
                pilares[self.destino].append(pilares[self.origen].pop())
            elif pilares[self.origen][-1] < pilares[self.destino][-1]: # es valido
                pilares[self.destino].append(pilares[self.origen].pop())
            else:
                print("No valido, el disco de origen es mayor al de destino")

    def Check(self):
        if self.pilar_3 == [6, 5, 4, 3, 2, 1]:
            print("lo has logrado")
        else:
            print("La torre de hanoi no ha sido completada")

    def __str__(self):
        output = ""
        # Range termina con -1 para recorrer al revés
        for i in range(5, -1, -1):
            fila = " "  # Armamos una fila a la vez, desde arriba
            # Pilar 1
            if len(self.pilar_1) > i:
                fila += str(self.pilar_1[i]) + " "
            else:
                fila += "x "
            # Pilar 2
            if len(self.pilar_2) > i:
                fila += str(self.pilar_2[i]) + " "
            else:
                fila += "x "
            # Pilar 3
            if len(self.pilar_3) > i:
                fila += str(self.pilar_3[i]) + " "
            else:
                fila += "x "
            output += fila + "\n"
        output += "=" * 7 + "\n"
        return output

torre = TorreDeHanoi()
print("Se inicia el desafio, ¿Estas Listo?")
while True:
    print(torre)
    print("Deseas hacer un movimiento (1) o chequear si esta lista (2)")
    decision = int(input())
    if decision == 1:
        print("escribe el pilar de origen y de destino respectivamente")
        ori = int(input())
        dest = int(input())
        torre.Mover_disco(ori, dest)
    elif decision == 2:
        torre.Check()
    else:
        print("Solo puedes elegir 1 o 2, donde 1 es mover un disco y 2 chequear si ganaste")
