def menu():
    '''
    Funcionalidad: Muestra el menú principal del programa y permite acceder a las diferentes opciones.
    Entrada: No recibe ningun dato
    Salida: No retorna ningun valor.
    '''
    tokens = []
    bitacora = []
    opcion = ""
    while opcion != "9":
        print("\n----- MENU -----")
        print("1. Cargar tokens")
        print("2. Mostrar tokens")
        print("3. Agregar/modificar tokens")
        print("4. Guardar tokens")
        print("9. Salir")
        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            tokens = cargarTokens(tokens, bitacora)
        elif opcion == "2":
            mostrarTokens(tokens)
        elif opcion == "3":
            tokens = agregarModificarTokens(tokens, bitacora)
        elif opcion == "4":
            guardarTokens(tokens, bitacora)
        elif opcion == "9":
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
    try:
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
                    for i in range(len(tokens)):
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
        for t in tokens:
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
    pares = cadena.split(",")
    for p in pares:
        if separador in p:
            partes = p.split(separador)
            original = partes[0].strip()
            reemplazo = partes[1].strip()
            encontrado = False
            for i in range(len(tokens)):
                if tokens[i][0] == original:
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
        with open(nombre, "w") as archivo:
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
    bitacora.append((fecha, accion))

menu()
