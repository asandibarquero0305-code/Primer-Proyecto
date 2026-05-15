def menu():
    '''
    Funcionalidad: Muestra el menú principal del programa y permite acceder a las diferentes opciones.
    Entrada: No recibe ningun dato
    Salida: No retorna ningun valor.
    '''
    tokens = []
    bitacora = []
    opcion = ""
    while opcion != "9": # El menú se repite hasta que el usuario decida salir con el 10
        print("1. Cargar tokens")
        print("2. Mostrar tokens")
        print("3. Agregar/modificar tokens")
        print("4. Guardar tokens")
        print("5. Traducir codigo")
        print("6. Generar CSV")
        print("7. Generar HTML")
        print("8. Filtrar por fecha")
        print("9. Filtrar por palabra")
        print("10. Salir")
        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            tokens = cargarTokens(tokens, bitacora)
        elif opcion == "2":
            mostrarTokens(tokens)
        elif opcion == "3":
            tokens = agregarModificarTokens(tokens, bitacora)
        elif opcion == "4":
            guardarTokens(tokens, bitacora)
        elif opcion == "5":
            estadisticas = traducirCodigo(tokens, bitacora)
        elif opcion == "6":
            generarCSV(estadisticas, bitacora)
        elif opcion == "7":
            generarHTML(estadisticas, bitacora)
        elif opcion == "8":
            filtrarPorFecha(bitacora)
        elif opcion == "9":
            filtrarPorPalabra(bitacora)
        elif opcion == "10":
            print("Saliendo...")
            registrar(bitacora, "Se salió del programa")
        else:
            print("Opcion invalida")

def cargarTokens(tokens, bitacora):
    '''
    Funcionalidad: Carga tokens desde un archivo de texto y los guarda en la lista de los tokens, evita duplicados.
    Entrada: tokens: lista con los tokens que se tienen hasta el momento.
            bitacora: lista donde se guardan los registros realizados.
    Salida: Retorna la lista de tokens actualizada.
    '''
    nombre = input("Ingrese el nombre del archivo: ")
    separador = input("Ingrese el separador (ej: ->): ")
    try: # Se abre el archivo en modo lectura para obtener los tokens
        with open(nombre, "r") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if separador in linea:
                    partes = linea.split(separador)
                    if len(partes) != 2:
                        print("Linea invalida:", linea)
                        continue
                    original = partes[0].strip()
                    reemplazo = partes[1].strip()
                    encontrado = False
                    for i in range(len(tokens)): # Se revisa si el token ya existe para evitar duplicados
                        if tokens[i][0] == original:
                            tokens[i] = (original, reemplazo)
                            encontrado = True
                            break
                    if not encontrado:
                        tokens.append((original, reemplazo))
        print("Tokens cargados correctamente")
        registrar(bitacora, "Se cargaron tokens")
    except:
        print("Error al abrir el archivo")
        registrar(bitacora, "Error al cargar archivo")
    return tokens

def mostrarTokens(tokens):
    '''
    Funcionalidad: Muestra todos los tokens almacenados hasta el momento en la memoria.
    Entrada: tokens: lista con los tokens que se tienen hasta el momento.
    Salida: No retorna ningun valor.
    '''
    if len(tokens) == 0:
        print("No hay tokens cargados")
    else:
        print("\n--- TOKENS ---")
        for t in tokens: # Se recorren todos los tokens almacenados para mostrarlos
            print(t[0], "->", t[1])

def agregarModificarTokens(tokens, bitacora):
    '''
    Funcionalidad: Permite agregar nuevos tokens o modificar los tokens existentes en la lista.
    Entrada: tokens: lista con los tokens que se tienen hasta el momento.
            bitacora: lista donde se guardan los registros realizados.
    Salida: Retorna la lista de tokens actualizada.
    '''
    cadena = input("Ingrese los tokens (ej: if->SI,for->PARA): ")
    separador = input("Separador (ej: ->): ")
    if cadena.strip() == "":
        print("Entrada vacia")
        return tokens
    pares = cadena.split(",") # Se separan los distintos pares de tokens ingresados
    for p in pares:
        if separador in p:
            partes = p.split(separador)
            original = partes[0].strip()
            reemplazo = partes[1].strip()
            encontrado = False
            for i in range(len(tokens)):
                if tokens[i][0] == original: # Si el token ya existe, solamente se actualiza el reemplazo
                    print("Token ya existe, se actualiza:", original)
                    tokens[i] = (original, reemplazo)
                    encontrado = True
                    registrar(bitacora, "Token actualizado: " + original)
                    break
            if not encontrado:
                print("Token agregado:", original)
                tokens.append((original, reemplazo))
                registrar(bitacora, "Token agregado: " + original)
        else:
            print("Formato incorrecto:", p)
    return tokens

def guardarTokens(tokens, bitacora):
    '''
    Funcionalidad: Guarda los tokens actuales en un archivo de texto.
    Entrada: tokens: lista con los tokens que se tienen hasta el momento.
            bitacora: lista donde se guardan los registros realizados.
    Salida: No retorna ningun valor.
    '''
    if len(tokens) == 0:
        print("No hay tokens para guardar")
        return
    nombre = input("Nombre del archivo: ")
    separador = input("Separador (ej: ->): ")
    try:
        with open(nombre, "w") as archivo: # Se crea o sobrescribe el archivo donde se guardarán los tokens
            for t in tokens:
                linea = t[0] + separador + t[1] + "\n"
                archivo.write(linea)
        print("Tokens guardados correctamente")
        registrar(bitacora, "Tokens guardados")
    except:
        print("Error al guardar archivo")
        registrar(bitacora, "Error al guardar archivo")

def registrar(bitacora, accion):
    '''
    Funcionalidad: Registra acciones realizadas por el usuario junto con la fecha y hora.
    Entrada: bitacora: lista donde se guardan los registros realizados. 
            accion: texto con la acción realizada.
    Salida: No retorna valores.
    '''
    from datetime import datetime
    fecha = datetime.now()
    bitacora.append((fecha, accion)) # Se guarda la fecha junto con la acción realizada

def traducirCodigo(tokens, bitacora):
    """Funcionalidad: Traduce un archivo usando los tokens que están cargados
    Entrada: Tokens=Lista de Tokens, Bitacora=Lista de registros
    Salida: Retorna estadisticas de reemplazos"""
    import re
    import time

    if len(tokens)==0:
        print("No hay tokens cargados actualmente")
        return{}
    
    archivoEntrada=input("Archivo de Entrada: ")
    archivoSalida=input("Archivo de Salida: ")

    reemplazo={}
    inicio=time.time()

    try:
        with open(archivoEntrada, "r")as entrada:
            lineas=entrada.readlines()
        resultado=[]
        cantidadDePalabras=0
        cantidadDeReemplazos=0
        for linea in lineas:
            palabras=re.findall(r'\w+|[^\w\s]', linea) # permite separar palabras y símbolos correctamente
            lineaNueva=""
            for palabra in palabras:
                if palabra.isnumeric():
                    lineaNueva+=palabra
                else:
                    reemplazada=False
                    for token in tokens:
                        original=token[0]
                        nuevo=token[1]
                        if palabra==original:
                            lineaNueva+=nuevo
                            reemplazada=True
                            cantidadDeReemplazos+=1
                            if original in reemplazo:
                                reemplazo[original]["cantidad"]+=1
                            else:
                                reemplazo[original]={"nuevo": nuevo,"cantidad": 1} #revisar este if, se supone q debería de reemplazar, *****hay q probar*****
                                registrar(bitacora, "Reemplazo realizado correctamente: "+original)
                                break
                    if not reemplazada:
                        lineaNueva+=palabra
                if palabra not in [".", ",", ":", ";", ")", "]", "}"]:
                    lineaNueva+=" "
                cantidadDePalabras+=1
            resultado.append(lineaNueva)
        with open(archivoSalida, "w") as salida:
            for linea in resultado:
                salida.write(linea+"\n")
        fin=time.time()
        duracion=fin-inicio
        porcentaje=0
        
        if cantidadDePalabras>0:
            porcentaje=(cantidadDeReemplazos/cantidadDePalabras)*100
        print("Se tradujo el codigo de manera correcta")
        registrar(bitacora,"Codigo Traducido")
        return {

            "reemplazos": reemplazo,
            "totalReemplazos": cantidadDeReemplazos,
            "totalPalabras": cantidadDePalabras,
            "porcentaje": porcentaje,
            "duracion": duracion
        }

    except:
        print("Error al traducir archivo")
        registrar(bitacora, "Error al traducir archivo")
    return {}

def generarCSV(estadisticas, bitacora):
    '''
    Funcionalidad: Genera un archivo CSV con las estadísticas de traducción.
    Entrada: Estadisticas: diccionario con estadísticas y reemplazos.
             Bitacora: Lista donde se guardan los registros realizados.
    Salida: No retorna valores.
    '''

    if estadisticas == {}:
        print("No hay datos para generar CSV")
        return
    nombre = input("Nombre del archivo CSV: ")
    try:
        with open(nombre, "w") as archivo:
            archivo.write("Original,Reemplazo,Cantidad\n")  # Se escriben los títulos de las columnas del CSV
            reemplazos = estadisticas["reemplazos"]
            for palabra in reemplazos:
                nuevo = reemplazos[palabra]["nuevo"]
                cantidad = reemplazos[palabra]["cantidad"]
                linea = palabra + "," + nuevo + "," + str(cantidad) + "\n"
                archivo.write(linea)
        print("CSV generado correctamente")
        registrar(bitacora, "CSV generado")
    except:
        print("Error al generar CSV")

def filtrarPorFecha(bitacora):
    '''
    Funcionalidad: Muestra Los registros de la bitácora según una fecha escogida.
    Entrada: Bitacora:Lista donde se guardan los registros realizados.
    Salida: No retorna valores.
    '''
    fechaBuscada = input("Ingrese la fecha (YYYY-MM-DD): ")
    encontrado = False
    for registro in bitacora:
        fecha = str(registro[0])
        if fechaBuscada in fecha:
            print(registro[0], "-", registro[1])
            encontrado = True
    if not encontrado:
        print("No se encontraron registros para esa fecha")

def filtrarPorPalabra(bitacora):
    '''
    Funcionalidad: Muestra registros de la bitácora que contengan una palabra clave.
    Entrada: Bitacora: lista donde se guardan los registros realizados.
    Salida: No retorna valores.
    '''
    palabra = input("Ingrese la palabra clave: ")
    encontrado = False
    for registro in bitacora:
        accion = registro[1]
        if palabra.lower() in accion.lower():
            print(registro[0], "-", accion)
            encontrado = True
    if not encontrado:
        print("No se encontraron registros")

def generarHTML(estadisticas, bitacora):
    '''
        Funcionalidad:
        Genera un archivo HTML con un reporte de la traduccion
        Entrada:
        estadisticas: diccionario con la información de los reemplazos y estadísticas.
        bitacora: lista donde se guardan los registros del sistema.
        Salida:
        No retorna valores.
        Genera un archivo HTML y registra la acción en la bitácora.
    '''
    from datetime import datetime
    if estadisticas == {}:
        print("No hay datos para generar HTML")
        return

    titulo = input("Titulo del reporte: ")
    fecha = datetime.now()
    nombre = "reporteHTML_" + fecha.strftime("%d-%m-%Y_%H-%M-%S") + ".html"

    try:
        with open(nombre, "w") as archivo:
            archivo.write("<html>\n")
            archivo.write("<head>\n")
            archivo.write("<title>" + titulo + "</title>\n")
            archivo.write("</head>\n")
            archivo.write("<body>\n")
            archivo.write("<h1>Reporte de Traduccion</h1>\n")
            archivo.write("<h2>")
            archivo.write(fecha.strftime("%d/%m/%Y %H:%M:%S"))
            archivo.write("</h2>\n")
            archivo.write("<p>Total reemplazos: " + str(estadisticas["totalReemplazos"]) + "</p>\n")
            archivo.write("<p>Porcentaje reemplazado: ")
            archivo.write(str(round(estadisticas["porcentaje"], 2)))
            archivo.write("%</p>\n")
            archivo.write("<p>Duracion: ")
            archivo.write(str(round(estadisticas["duracion"], 2)))
            archivo.write(" segundos</p>\n")
            archivo.write("<table border='1'>\n") # Se crea una tabla para mostrar las estadísticas
            archivo.write("<tr>")
            archivo.write("<th>Original</th>")
            archivo.write("<th>Reemplazo</th>")
            archivo.write("<th>Cantidad</th>")
            archivo.write("</tr>\n")

            reemplazos = estadisticas["reemplazos"]
            color = True

            for palabra in reemplazos:
                if color:
                    archivo.write("<tr bgcolor='lightgray'>")
                else:
                    archivo.write("<tr bgcolor='white'>")

                archivo.write("<td align='center'>" + palabra + "</td>")
                archivo.write("<td align='center'>")
                archivo.write(reemplazos[palabra]["nuevo"])
                archivo.write("</td>")
                archivo.write("<td align='center'>")
                archivo.write(str(reemplazos[palabra]["cantidad"]))
                archivo.write("</td>")
                archivo.write("</tr>\n")

                color = not color

            archivo.write("</table>\n")
            archivo.write("</body>\n")
            archivo.write("</html>\n")

        print("Reporte HTML generado")
        registrar(bitacora, "Reporte HTML generado")

    except:
        print("Error al generar HTML")
        registrar(bitacora, "Error al generar HTML")
# programa principal
menu()
