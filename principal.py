"""
Grupo P2 3
Grover Eduardo Ugarte Quispe 202020159
Daniel Arturo Ventura Atarama 202010429
Miguel Apaza Pariona
"""

import funciones
from os import system
import json

def main():

    system("clear")

    controlAbandondo=[0,0,0] #controla la manipulación de opciones salir y regresar

    archivoJSON=open("config.json",)
    cargaJSON=json.load(archivoJSON) #se accede al json 
    dificultad=cargaJSON["dificultad"] #consigue dificultad
    archivoJSON.close()

    funciones.fM.menuPrincipal(controlAbandondo, dificultad)

    cargaJSON["dificultad"]=dificultad #actualizar dificultad
    cargaJSON=json.dumps(cargaJSON, indent=4, separators=(", ", " : "))

    nuevoJSON=open("config.json","w")
    nuevoJSON.write(cargaJSON)
    system("clear")

main()
