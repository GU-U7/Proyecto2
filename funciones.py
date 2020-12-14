import jugabilidad
from os import system
import pandas as pd
import random 
import time
import json
import webbrowser

archivoJSON=open("config.json",)
configJSON=json.load(archivoJSON)
archivoJSON.close() 

class funcionesMain:

    def __init__(self, archivoJSON): #Definimos variables locales para facilitar el acceso a los valores JSON
        self.configMenuPrincipal=archivoJSON["funcMain"]["menuPrincipal"]
        self.configMenuJugar=archivoJSON["funcMain"]["menuJugar"]
        self.configMenuConfiguracion=archivoJSON["funcMain"]["menuConfiguracion"]
        self.configOpcion=archivoJSON["funcMain"]["opcion"]
        self.configMiscelacneo=archivoJSON["funcMain"]["miscelaneo"]
        self.columnas=archivoJSON["configuraciones"]["columnas"]
        self.dificultades=archivoJSON["configuraciones"]["dificultades"]

    def resultadosLeer(self):
        system("clear")
        columnas_resultados=self.columnas
        archivo = pd.read_csv("resultados.csv",names=columnas_resultados, header=None)
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
                otraVez="Si"
                while otraVez=="Si":
                    resultados=jugabilidad.juegoUnJugador(dificultad)
                    self.resultadosGrabar(resultados)
                    if resultados["Estado final"]=="Gano":
                        print(self.configMenuJugar[4])
                        otraVez=self.opcionValidar(["Si","No"])
                        if otraVez=="Si" and not dificultad[0]==self.dificultades[2]:
                            if dificultad[0]==self.dificultades[0]:
                                dificultad[0]=self.dificultades[1]
                            else:
                                dificultad[0]=self.dificultades[2]
                    else:
                        otraVez="No"
                system("clear")
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
                print(self.configMenuConfiguracion[5])
                print(self.configMenuConfiguracion[9], dificultad[2])
                dificultad[2] = int(self.opcionValidar([str(5*a) for a in range(1,19)]))
                system("clear")
            elif opcionConfig == "2":
                system("clear")
                print(self.configMenuConfiguracion[6])
                print(self.configMenuConfiguracion[7], dificultad[0])
                dificultad[0] = self.opcionValidar([self.dificultades[0], self.dificultades[1], self.dificultades[2]])
                system("clear")
            elif opcionConfig == "3":
                system("clear")
                print(self.configMenuConfiguracion[8])
                print(self.configMenuConfiguracion[7], dificultad[1])
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

        #Se actualizan y graban los resultados 
        columnas_resultados=self.columnas
        df=pd.read_csv("resultados.csv",names=columnas_resultados, header=None)
        df=df.append(resultados,ignore_index=True)


        entradas=[]
        for i in range(0,df.shape[0]):
            entradas.append(dict(df.loc[i]) )

        def quicksort(A,p,r):
            if p<r:
                q=particion(A,p,r)
                quicksort(A,p,q-1)
                quicksort(A,q+1,r)

        def particion(A,p,r):
            x=A[r][columnas_resultados[1]]
            i=p-1
            for j in range(p, r):
                if A[j][columnas_resultados[1]]>=x:
                    i+=1
                    A[i],A[j]=A[j],A[i]
            A[i+1],A[r]=A[r],A[i+1]
            return i+1

        quicksort(entradas, 0, len(entradas)-1)

        pd.DataFrame(entradas).loc[:9].to_csv("resultados.csv", index=False, header=False)        

    

class funcionesJuego:

    alfabeto=[chr(a) for a in range(97, 123)] + [chr(b) for b in range(65,91)]+[str(n) for n in range(0,10)]

    def __init__(self, archivoJSON): #Definimos variables locales para facilitar el acceso a los valores JSON
        self.configResultados=archivoJSON["funcJuego"]["resultados"]
        self.configPalabraImprimir=archivoJSON["funcJuego"]["palabraImprimir"]
        self.configCaracterObtener=archivoJSON["funcJuego"]["caracterObtener"]
        self.configIgnorar=archivoJSON["funcJuego"]["ignorar"]
        self.dificultades=archivoJSON["configuraciones"]["dificultades"]

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

        if dificultad==self.dificultades[0]:
            seleccion=palabras[random.randint(3,5)] if random.randint(1,100)<=int(probabilidad*100) else palabras[random.randint(0,5)]
        elif dificultad==self.dificultades[1]:
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
        print(self.configPalabraImprimir)
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
        if caracter=="Proyecto2":
            webbrowser.open("http://www1.herrera.unt.edu.ar/biblcet/wp-content/uploads/2014/12/ippython.pdf")
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

    def dibujar(self,intentos, errores):
        #MARCO SUPERIOR
        for i in range(intentos+3):
            print("=",end="")
        print()
        #PALO SUPERIOR
        for i in range(intentos+2):
            if i <(intentos//5)*2:
                print(" ", end="")
            elif i==(intentos//5)*2 or i==intentos+1:
                print("+",end="")
            else:
                print("-",end="")
        print()
        #PALOS LATERALES
        for i in range(intentos+2):
            if i==(intentos//5)*2 or i==intentos+1:
                print("|",end="")
            else:
                print(" ",end="")
        print()
        #CABEZA
        for i in range(intentos+2):
            if i==(intentos//5)*2:
                print("O",end="")
            elif  i==intentos+1:
                print("|",end="")
            else:
                print(" ",end="")
        print()
        #CUERPO
        flag1=intentos//5+(intentos//5-1)
        flag2=intentos//5+(intentos//5+1)
        conteo=0
        for i in range(((intentos)//5)*2):
            for j in range(intentos+2):
                if j==intentos+1:
                    print("|",end="")
                elif j in range(intentos//5,(intentos//5)*3+1):
                    if j==flag1:
                        if conteo<errores:
                            print('/',end='')
                            conteo+=1
                        else:
                            print(' ',end='')
                        flag1-=1
                    elif j==flag2:
                        if conteo<errores:
                            print('\\',end='')
                            conteo+=1
                        else:
                            print(' ',end='')
                    elif j ==2*intentos//5 and i<(intentos)//5:
                        if conteo<errores:
                            print("|",end="")
                            conteo+=1
                        else:
                            print(' ',end='')
                    else:
                        print(" ",end="") #Espacios de casilla de la persona
                else:
                    print(" ",end="")
            
            flag2+=1
            if flag1<intentos//5:
                flag1=intentos//5+(intentos//5-1)
                flag2=intentos//5+(intentos//5+1)
            print()
        #PALO
        for i in range(intentos+2):
            if i==intentos+1:
                print("|",end="")
            else:
                print(" ",end="")
        print()
        #MARCO INFERIOR
        for i in range(intentos+3):
            print("=",end="")
        print()

    def ignorar(self):
        a=input(self.configIgnorar)

fM=funcionesMain(configJSON)
fJ=funcionesJuego(configJSON)