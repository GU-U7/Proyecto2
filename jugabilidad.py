import funciones
import os

def juegoUnJugador(dificultad):
    palabra, palabraMuestra = funciones.fJ.palabraSeleccionada(dificultad[0], dificultad[1])
    errores = 0
    puntaje = 0
    tiempo = [0]

    while not errores==dificultad[2]:
        os.system("clear")
        funciones.fJ.dibujoN(dificultad[2], errores)
        funciones.fJ.palabraImprimir(palabraMuestra)

        if funciones.fJ.palabraCompleta(palabraMuestra, palabra):
            nombre=funciones.fJ.resultados(puntaje, tiempo, 'G')
            funciones.fJ.ignorar()
            os.system("clear")
            return [nombre[:5], puntaje, round(tiempo[0],2), "Gano",  dificultad[2],  errores]
      
        letra=funciones.fJ.caracterObtener(tiempo)
        
        if funciones.fJ.caracterComprobar(letra, palabra):
            if not ((letra.lower() in palabraMuestra) or (letra.upper() in palabraMuestra)):
                puntaje+=1
            funciones.fJ.caracterReemplazar(letra, palabraMuestra, palabra)   
        else:
            errores+=1
    else:
        os.system("clear")
        funciones.fJ.dibujoN(dificultad[2], errores)
        funciones.fJ.palabraImprimir(palabraMuestra)
        nombre=funciones.fJ.resultados(puntaje, tiempo, 'P')
        funciones.fJ.ignorar()
        os.system("clear")
        return [nombre[:5], puntaje, round(tiempo[0],2), "Perdio",  dificultad[2],  dificultad[2]]
