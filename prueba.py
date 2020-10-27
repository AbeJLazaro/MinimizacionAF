'''
Autor:            Lázaro Martínez Abraham Josué
Fecha versión:    26-10-2020
Programa:         prueba del algoritmo de minimización
'''

from minimizacion import miminizar
from leerTabla import leerDatos

nombre = input("Ingresa el nombre del archivo:\n")
#nombre = "tabla.csv"

tabla = leerDatos(nombre)
agrupaciones,tablaMinima = miminizar(tabla)
print(agrupaciones)
for i in tablaMinima:
    print(i,":",tablaMinima[i])
