def menu():
    tokens = []
    opcion = ""

    while opcion != "9":
        print("\n--- MENU ---")
        print("1. Cargar tokens")
        print("2. Mostrar tokens")
        print("3. Agregar/modificar tokens")
        print("9. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            tokens = cargarTokens(tokens)
        elif opcion == "2":
            mostrarTokens(tokens)
        elif opcion=="3":
            tokens=agregarModificarTokens(tokens)
        elif opcion == "9":
            print("Saliendo...")
        else:
            print("Opcion invalida")


def cargarTokens(tokens):
    nombre = input("Ingrese el nombre del archivo: ")
    separador = input("Ingrese el separador (ej: ->): ")

    try:
        with open(nombre, "r") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if separador in linea:
                    partes = linea.split(separador)
                    original = partes[0].strip()
                    reemplazo = partes[1].strip()
                    tokens.append((original, reemplazo))
        print("Tokens cargados correctamente")
    except:
        print("Error al abrir el archivo")

    return tokens


def mostrarTokens(tokens):
    if len(tokens) == 0:
        print("No hay tokens cargados")
    else:
        print("\nTokens:")
        for t in tokens:
            print(t[0], "->", t[1])

def agregarModificarTokens(tokens):
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
                    break

            if not encontrado:
                print("Token agregado:", original)
                tokens.append((original, reemplazo))
        else:
            print("Formato incorrecto:", p)

    return tokens

# programa principal
menu()

