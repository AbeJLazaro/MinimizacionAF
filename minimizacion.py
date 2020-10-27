'''
Autor:            Lázaro Martínez Abraham Josué
Fecha versión:    26-10-2020
Programa:         Implementación del algoritmo de minimización de un
                  AF
'''

# función que nos ayudará a encontrar en que grupo se encuentra el estado
def buscarEstado(estadoObjetivo,grupos):
  '''Esta función nos regresa a que grupo de estados pertenece un estado

  Parámetros
  estadoObjetivo: estado a buscar dentro de los grupos de estados
  grupos: Diccionario de agrupaciones
  
  return: agrupación a la que pertenece un estado 
  '''

  '''
  Se vería de esta forma en la primer iteración:
    {
      "1": [lista de estados de aceptación],
      "2": [lista de estados de no aceptación]
    }
  Regresará la llave que representa a la lista a la que pertenece un
  estado. Esta forma cambiará conforme pasan las iteraciones
  '''
  # se visita a cada llave y valor del diccionario grupo
  for agrupación,listaEstadosOriginales in grupos.items():
    # si el estado objetivo se encuentra en la lista de estados de un item del
    # diccionario grupo
    if estadoObjetivo in listaEstadosOriginales:
      # regresa el número de la agrupación a la que pertenece
      return agrupación

def miminizar(transiciones):
  '''Función minimiza una tabla de transiciones de un AFD

  Parámetros 
  transiciones: tabla de transiciones (diccionario)

  return: agrupaciones y tabla de transiciones minima

  '''

  # primera division entre los estados que son de aceptación y los que no
  # para esto utilizaremos la información del elemento "aceptación" en la tabla
  # de transición de cada estado
  grupo={"1":[],"2":[]}

  # para todas las llaves (estados) en el diccionario transiciones
  for key in transiciones.keys():
    # el diccionario para esa llave nos regresa la tabla de transiciones
    # del estado, otro diccionario, por lo cual visitamos el miembro "aceptación"
    # Sí es un estado de aceptación
    if transiciones[key]["aceptación"]:
      # anexamos el estado en cuestión, representado por key, al grupo 1
      grupo["1"].append(key)
    # sí no es un estado de aceptación
    else:
      # anexamos el estado en cuestión, representado por key, al grupo 2
      grupo["2"].append(key)

  while True:
    # se genera un diccionario que nos ayudará a guardar las nuevas
    # transiciones para cada estado
    estadosCambiados = {}

    # se visita el estado y la tabla de transición de cada estado en la
    # tabla original
    for estado,trans in transiciones.items():
      '''La tabla de transición de cada estado es otro diccionario
        estado: transiciones
        "0"   : {"a":"1","b":"1","c":"4"}
        Lo que haremos a continuación es tomar cada llave del diccinario que
        representa las transiciones: caracteres ("a","b","c") y los estados 
        a los que llega mediante esos caracteres ("1","1","4")

        Con ayuda de la función buscarEstado() encontraremos en la tabla de
        grupo, a que agrupación pertenece dicho estado al que llega con cada 
        caracter, para escribir un diccionario nuevo que tenga representado
        con que caracter llega a que agrupación
      '''
      nuevasTransiciones = dict([(x,buscarEstado(y,grupo)) \
        for x,y in list(trans.items())[:-1]])
      nuevasTransiciones["aceptación"]=trans["aceptación"]
      # agregamos este estado con sus nuevas transiciones al diccinario 
      # estadosCambiados
      estadosCambiados[estado]=nuevasTransiciones

    # una vez que tengamos las transiciones con las agrupaciones
    # generamos un diccionario auxiliar para agregar las nuevas 
    # agrupaciones
    grupoP={}
    # contador para nombrar a los grupos
    i=0
    # para cada estado y sus transiciones del diccinario estadosCambiados
    for estado,trans in estadosCambiados.items():
      # comparamos si aun no existen agrupaciones nuevas
      if len(grupoP)<1:
        # sí no existen agrupaciones nuevas, generamos la primer entrada
        # el nombre de la agrupación esta dada por el contador i y 
        # recordemos que esta agrupación tendra asociada una lista de estados
        # que la componen
        grupoP[str(i)]=[estado]
        # aumentamos el valor de i
        i+=1
      # si ya existe por lo menos una nueva agrupación
      else:
        # ponemos una bandera que nos indicará si se agregó o no el estado a alguna
        # agrupación
        bandera = True
        # para cada nueva agrupación en el diccionario grupoP
        for key in grupoP:
          # primer estado en el diccionario grupoP de una agrupación
          primerEstado = grupoP[key][0]
          # comparamos si las nuevas transiciones de este primer estado son iguales
          # a las transiciones del estado que busca agregarse a una agrupación
          A = str(estadosCambiados[primerEstado]) == str(trans)
          # si se cumplen las comparaciones, se agrega a la agrupación visitada
          if A:
            # se cambia el valor de la bandera
            bandera = False
            grupoP[key].append(estado)
        # si termina el ciclo y el valor de la bandera no cambió, se agrega una nueva
        # entrada a las nuevas agrupaciones
        if bandera:
          grupoP[str(i)]=[estado]
          i+=1
    # si el diccionario de agrupaciones nuevo es igual al diccionario de agrupaciones
    # anterior, rompemos el ciclo
    if str(grupo)==str(grupoP):
      break
    # se sustituye el diccionario de agrupaciones por el nuevo diccionario de
    # agrupaciones
    grupo = grupoP.copy() 

  # parte de la función para crear la nueva tabla de transiciones
  transicionesMinimas = {}
  for key,lista in grupo.items():
    trans = estadosCambiados[lista[0]]
    transicionesMinimas[key]=trans
    bandera = False
    for estado in lista:
      if transiciones[estado]["inicio"]:
        bandera = True
    transicionesMinimas[key]["inicio"]=bandera


  return grupo,transicionesMinimas

if __name__ == '__main__':
  # tabla de estados
  '''Campos importantes:
    La llave principal indica el identificador del estado
    Los diccionarios internos indican las transiciones
    y si se trata de un estado de aceptación o no'''

  '''
  # prueba 1
  transiciones = {
    "0" : {"a": "1","b":"2","aceptación":False,"inicio":True},
    "1" : {"a": "1","b":"3","aceptación":False,"inicio":False},
    "2" : {"a": "1","b":"2","aceptación":False,"inicio":False},
    "3" : {"a": "1","b":"4","aceptación":False,"inicio":False},
    "4" : {"a": "1","b":"2","aceptación":True,"inicio":False}
  }
  '''

  # prueba 2
  transiciones = {
    #estado : tabla de transición
    "0" : {"a": "1","b":"2","aceptación":True,"inicio":True},
    "1" : {"a": "0","b":"3","aceptación":False,"inicio":False},
    "2" : {"a": "3","b":"0","aceptación":False,"inicio":False},
    "3" : {"a": "4","b":"5","aceptación":False,"inicio":False},
    "4" : {"a": "3","b":"6","aceptación":False,"inicio":False},
    "5" : {"a": "6","b":"3","aceptación":False,"inicio":False},
    "6" : {"a": "7","b":"8","aceptación":True,"inicio":False},
    "7" : {"a": "6","b":"3","aceptación":False,"inicio":False},
    "8" : {"a": "3","b":"6","aceptación":False,"inicio":False}
  }

  '''
  # prueba 3
  transiciones = {
    #estado : tabla de transición
    "0" : {"a": "1","b":"2","aceptación":False,"inicio":True},
    "1" : {"a": "0","b":"3","aceptación":False,"inicio":False},
    "2" : {"a": "3","b":"0","aceptación":True,"inicio":False},
    "3" : {"a": "4","b":"5","aceptación":False,"inicio":False},
    "4" : {"a": "3","b":"6","aceptación":True,"inicio":False},
    "5" : {"a": "6","b":"3","aceptación":False,"inicio":False},
    "6" : {"a": "7","b":"8","aceptación":False,"inicio":False},
    "7" : {"a": "6","b":"3","aceptación":False,"inicio":False},
    "8" : {"a": "3","b":"6","aceptación":True,"inicio":False}
  }
  '''
  g,t=miminizar(transiciones)
  print(g)
  for i in t:
    print(t[i])