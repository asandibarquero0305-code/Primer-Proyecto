def menu():
    tokens = []
    bitacora = []
    opcion = ""
    while opcion != "9":
        print("\n--- MENU ---")
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
    if len(tokens) == 0:
        print("No hay tokens cargados")
    else:
        print("\n--- TOKENS ---")
        for t in tokens:
            print(t[0], "->", t[1])

def agregarModificarTokens(tokens, bitacora):
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
    from datetime import datetime
    fecha = datetime.now()
    bitacora.append((fecha, accion))

menu()
