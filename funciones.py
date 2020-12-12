import jugabilidad
from os import system
import pandas as pd
import random 
import time
import json

archivoJSON=open("config.json",)
configJSON=json.load(archivoJSON)
archivoJSON.close() 

class funcionesMain:

    def __init__(self, archivoJSON):
        self.configMenuPrincipal=archivoJSON["funcMain"]["menuPrincipal"]
        self.configMenuJugar=archivoJSON["funcMain"]["menuJugar"]
        self.configMenuConfiguracion=archivoJSON["funcMain"]["menuConfiguracion"]
        self.configOpcion=archivoJSON["funcMain"]["opcion"]
        self.configMiscelacneo=archivoJSON["funcMain"]["miscelaneo"]

    def resultadosLeer(self):
        system("clear")
        archivo = pd.read_csv("resultados.csv")
        print(archivo)
        del archivo

    def opcionValidar(self, opciones):
        opcion=input(self.configOpcion[0]) 
        while not opcion in opciones:
            opcion=input(self.configOpcion[1])
        return opcion

    def menuPrincipal(self,opciones, dificultad):
        system("clear")
        while opciones[2]==0:
            print("1.",self.configMenuPrincipal[0])
            print("2.",self.configMenuPrincipal[1])
            print("3.",self.configMenuPrincipal[2])
            print("4.",self.configMenuPrincipal[3])
            opcionPrincipal=self.opcionValidar(["1","2","3","4"])
            if opcionPrincipal == "1":
                self.menuJugar(opciones, dificultad)
            elif opcionPrincipal == "2":
                self.menuConfiguracion(opciones, dificultad)
            elif opcionPrincipal == "3":
                self.resultadosLeer()
                print("1.",self.configMiscelacneo[1])
                regresar=self.opcionValidar(['1'])
                system("clear")
            else:
                opciones[2]=1
        system("clear")

    def menuJugar(self,opciones, dificultad):
        system("clear")
        while opciones[2]==0 and opciones[0]==0:
            print("1.",self.configMenuJugar[0])
            print("2.",self.configMenuJugar[1])
            print("3.",self.configMenuJugar[2])
            print("4.",self.configMenuJugar[3])
            opcionJugar=self.opcionValidar(["1","2","3","4"])
            if opcionJugar=="1":
                resultados=jugabilidad.juegoUnJugador(dificultad)
                self.resultadosGrabar(resultados)
            elif opcionJugar=="2":
                system("clear")
                print(self.configMiscelacneo[0])
                print("1.",self.configMiscelacneo[1])
                regresar=self.opcionValidar(['1'])
                system("clear")
            elif opcionJugar=="3":
                opciones[0]=1
            else:
                opciones[2]=1
        opciones[0]=0
        system("clear")

    def menuConfiguracion(self,opciones, dificultad):
        system("clear")
        while opciones[2]==0 and opciones[1]==0:
            print("1.",self.configMenuConfiguracion[0])
            print("2.",self.configMenuConfiguracion[1])
            print("3.",self.configMenuConfiguracion[2])
            print("4.",self.configMenuConfiguracion[3])
            print("5.",self.configMenuConfiguracion[4])
            opcionConfig=self.opcionValidar(["1","2","3","4","5"])
            if opcionConfig == "1":
                system("clear")
                print("Cantidad de intentos para el juego (solo puede ser 5, 10 o 15):")
                print("Intentos actuales:", dificultad[2])
                dificultad[2] = int(self.opcionValidar(["5", "10", "15"]))
                system("clear")
            elif opcionConfig == "2":
                system("clear")
                print("Ingresar dificultad ya sea Facil(F), Medio(M) o Dificil(D):")
                print("Dificultad actual:", dificultad[0])
                dificultad[0] = self.opcionValidar(["F", "M", "D"])
                system("clear")
            elif opcionConfig == "3":
                system("clear")
                print("Ingresar probabilidad (enteros del 0 al 100):")
                print("Dificultad actual:", dificultad[1])
                dificultad[1] = int(input())
                while not dificultad[1] in range(0,100):
                    dificultad[1] = int(input())
                dificultad[1]/=100
                system("clear")
            elif opcionConfig == "4":
                opciones[1] = 1
            elif opcionConfig == "5":
                opciones[2] = 1
        opciones[1]=0
        system("clear")

    def resultadosGrabar(self, resultados):
        archivo = open("resultados.csv", "a")
        for i in range(len(resultados)-1):
            archivo.write(str(resultados[i])+", ")
        archivo.write(str(resultados[len(resultados)-1])+"\n")
        archivo.close()

    

class funcionesJuego:

    alfabeto=[chr(a) for a in range(97, 123)] + [chr(b) for b in range(65,91)]+[str(n) for n in range(0,10)]

    def __init__(self, archivoJSON):
        self.configResultados=archivoJSON["funcJuego"]["resultados"]
        self.configPalabraSeleccionada=archivoJSON["funcJuego"]["palabraSeleccionada"]
        self.configCaracterObtener=archivoJSON["funcJuego"]["caracterObtener"]
        self.configIgnorar=archivoJSON["funcJuego"]["ignorar"]

    def resultados(self,puntaje, tiempo, estado):
        if estado=='G':
            print(self.configResultados["estado"][0])
        else:
            print(self.configResultados["estado"][1])
        print(self.configResultados["puntaje"],puntaje)
        print(self.configResultados["tiempo"],round(tiempo[0],2),"s")
        nombre=input(self.configResultados["nombre"][0])
        while len(nombre)<1 or len(nombre)>20:
            nombre=input(self.configResultados["nombre"][1])
        return nombre

    def palabraSeleccionada(self, dificultad, probabilidad):
        entradas=open("entradas.txt", "r")
        palabras=[i[:len(i)-1] for i in entradas]
        entradas.close()

        if dificultad=="Facil":
            seleccion=palabras[random.randint(3,5)] if random.randint(1,100)<=int(probabilidad*100) else palabras[random.randint(0,5)]
        elif dificultad=="Medio":
            seleccion=palabras[19] if random.randint(1,100) <= int(probabilidad*100) else palabras[random.randint(6,19)]
        else:
            seleccion=palabras[20]

        seleccionLista=[]
        for i in seleccion:
            if i==' ':
                seleccionLista.append('|')
            else:
                seleccionLista.append('_')
        return seleccion, seleccionLista

    def palabraImprimir(self,lista):
        print(self.configPalabraSeleccionada)
        for i in lista:
            print(i,end=' ')
        print()

    def palabraCompleta(self,lista, original):
        for i in range(len(original)):
            if not (lista[i]==original[i] or lista[i]=='|'):
                return False
        return True

    def caracterObtener(self,tiempo):
        tiempoInicial=time.time()
        caracter=input(self.configCaracterObtener)
        while len(caracter)!=1 or not caracter in self.alfabeto:
            caracter=input(self.configCaracterObtener)
        tiempoFinal=time.time()
        tiempo[0]+=(tiempoFinal-tiempoInicial)
        caracter=caracter.lower()
        return caracter

    def caracterComprobar(self,caracter,original):
        if caracter in original or caracter.upper() in original:
            return True
        return False

    def caracterReemplazar(self,caracter, lista, original):
        for i in range(len(original)):
            if caracter==original[i] or caracter.upper()==original[i]:
                lista[i]=original[i]

    def dibujo5(self,errores):
        C1=["   ",' | ','/| ', '/|\\']
        C2=["   ","/  ","/ \\"]
        print("========")
        print("  +---+")
        print("  |   |")
        print("  O   |")
        print(" "+C1[3 if errores>=3 else errores]+"  |")
        print(" "+C2[0 if errores<4 else errores%3]+"  |")
        print("      |")
        print("========")

    def dibujo10(self,errores):
        C1=['   ',' | ','/| ', '/|\\']
        C2=['     ','  |  ','/ |  ','/ | \\']
        C3=['   ','/  ','/ \\']
        C4=['     ','/    ','/   \\']
        print("============")
        print("    +------+")
        print("    |      |")
        print("    O      |")
        print("   "+C1[3 if errores>=3 else errores]+"     |")
        print("  "+C2[0 if errores<4 else (3 if errores>6 else errores-3)]+"    |")
        print("   "+C3[0 if errores<7 else (2 if errores>8 else errores%6)]+"     |")
        print("  "+C4[0 if errores<9 else errores%8]+"    |")
        print("           |")
        print("           |")
        print("============")

    def dibujo15(self,errores):
        C1=["   "," | ","/| ","/|\\"]
        C2=["     ","  |  ","/ |  ","/ | \\"]
        C3=["       ","   |   ","/  |   ","/  |  \\"]
        C4=["   ","/  ","/ \\"]
        C5=["     ","/    ","/   \\"]
        C6=["       ","/      ","/     \\"]
        print("====================")
        print("      +-----------+")
        print("      |           |")
        print("      O           |")
        print("     "+C1[3 if errores>3 else errores]+"          |")
        print("    "+C2[0 if errores<4 else (3 if errores>6 else errores-3)]+"         |")
        print("   "+C3[0 if errores<7 else (3 if errores>9 else errores-6)]+"        |")
        print("     "+C4[0 if errores<10 else (2 if errores>11 else errores-9)]+"          |")
        print("    "+C5[0 if errores<12 else (2 if errores>13 else errores-11)]+"         |") 
        print("   "+C6[0 if errores<14 else errores-13]+"        |")
        print("                  |")
        print("                  |")
        print("                  |")
        print("====================")

    def dibujoN(self,intentos, errores):
        if intentos==5:
            self.dibujo5(errores)
        elif intentos==10:
            self.dibujo10(errores)
        else:
            self.dibujo15(errores)

    def ignorar(self):
        a=input(self.configIgnorar)

fM=funcionesMain(configJSON)
fJ=funcionesJuego(configJSON)