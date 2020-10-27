'''
Autor:            Lázaro Martínez Abraham Josué
Fecha versión:    26-10-2020
Programa:         Implementación de una función para leer una tabla 
                  que representa una tabla de transiciones del AF 
'''

def leerDatos(nombre):
  '''Función que lee el archivo de la tabla de transición
  para representarla en forma de diccionarios para después
  minimizarlos

  Parámetros
  nombre: nombre del archivo

  return: tabla de transición
  '''
  
  try:
    # se lee el archivo
    File = open(nombre,"r")
    datos = File.readlines()
    File.close()

  except IOError as ioe:
    print("Error al abrir el archivo")
    print(ioe)
    return 
  except Exception as e:
    print("Ocurrió otro error")
    raise e
  else:
    # se quitan los saltos de línea
    for i in range(len(datos)):
      datos[i]=datos[i].replace("\n","")

    # se rescatan los caracteres
    caracteres = datos.pop(0).split(",")[1:]
    
    # se inicializa la tabla de transiciones
    tablaTransicion={}

    # para cada línea en la lista de datos
    for línea in datos:
      # se separan los datos por medio de las comas
      información = línea.split(",")

      # se saca el primer elemento separado que representa el estado
      estado = información.pop(0)

      # se genera la lista de transiciones con la información restante y
      # la lista de caracteres
      listaTransicion=dict(zip(caracteres,información))

      # se revisa si el estado tiene un * para representar en la tabla que 
      # se trata de un estado de aceptación
      if "*" in estado:
        listaTransicion["aceptación"]=True
        estado = estado.replace("*","")
      else:
        listaTransicion["aceptación"]=False


      if "->" in estado:
        listaTransicion["inicio"]=True
        estado = estado.replace("->","")
      else:
        listaTransicion["inicio"]=False
      # se agrega esta información a la tabla de transiciones
      tablaTransicion[estado]=listaTransicion

    return tablaTransicion

if __name__ == '__main__':
  nombre = "tabla.csv"
  a=leerDatos(nombre)
  for estado,transiciones in a.items():
    print(estado,":",transiciones)