
biblioteca = {
    1: {"titol": "Python per a tothom", "autor": "John Doe", "quantitat": 3},
    2: {"titol": "Dades i Estructures", "autor": "Anna Smith", "quantitat": 5},
    3: {"titol": "Introducció a OOP", "autor": "Joan Costa", "quantitat": 2},
}

def afegir_llibre(biblioteca, id_llibre, titol, autor, quantitat):

    if id_llibre in biblioteca:
        print(f"El ID del llibre {id_llibre} ja es a la biblio!")
    else:
        biblioteca[id_llibre] = {
            "titol": titol,
            "autor":autor,
            "quantiat":quantitat
        }
        print(f"Llibre {titol} afegit amb éxit")

def buscar_llibre(biblioteca, id_llibre):

    if id_llibre in biblioteca:
        llibre = biblioteca[id_llibre]
        print(f"ID: {id_llibre}")
        print(f"Títol: {llibre['titol']}")
        print(f"Autor: {llibre['autor']}")
        print(f"Quantitat: {llibre['quantitat']}")
    else:
        print("El llibre no existeix!")

def mostrar_llibres(biblioteca):

    if not biblioteca:
        print("No hi ha llibres disponibles a la biblioteca.")
        return

    print("Llibres disponibles:")
    for id_llibre, info in biblioteca.items():
        print(f"ID: {id_llibre}")
        print(f"Títol: {info['titol']}")
        print(f"Autor: {info['autor']}")
        print(f"Quantitat: {info['quantitat']}")
        print("------------------------------------")  # separador


def prestar_llibre(biblioteca, id_llibre):
    if id_llibre in biblioteca:
        if biblioteca[id_llibre]['quantitat'] > 0:
            biblioteca[id_llibre]['quantitat'] -= 1
            print(f"Préstec confirmat: Has pres el llibre '{biblioteca[id_llibre]['titol']}'.")
            print(f"Queden {biblioteca[id_llibre]['quantitat']} exemplars disponibles.")
        else:
            print(f"Error: No hi ha llibres disponibles per al llibre '{biblioteca[id_llibre]['titol']}'.")



while True:
    print("\nBIBLIOTECA")
    print("-" * 20)
    print("1. Afegir llibre")
    print("2. Buscar llibre")
    print("3. Mostrar tots els llibres")
    print("4. Prestec del llibre")
    print("5. Sortir")

    seleccio = input("Introdueix la teva selecció: ")

    if seleccio == '1':
        try:
            id_llibre = int(input("Introdueix el ID del llibre nou:"))
            titol = input("Introdueix títol del llibre: ")
            autor = input("Introdueix l'autor")
            quantitat = int(input("Introdueix la quantitat"))
            afegir_llibre(biblioteca, id_llibre, titol, quantitat)
            input("Prem Enter per continuar...")
        except ValueError:
            print("No es un caràcter vàlid!")

    elif seleccio == '2':
        try:
            id_llibre = int(input("Introdueix l'ID del llibre a buscar: "))
            buscar_llibre(biblioteca,id_llibre)
            input("Prem Enter per continuar...")
        except ValueError:
            "No vàlid!"
    elif seleccio == '3':
        mostrar_llibres(biblioteca)
        input("Prem Enter per continuar...")

    elif seleccio == '4':
        try:
            id_llibre = int(input("Introdueix ID del llibre que vols prestar: "))
            prestar_llibre(biblioteca,id_llibre)
            input("Prem Enter per continuar...")
        except ValueError:
            "No vàlid!"
    elif seleccio == '5':
        print("Sortint...")
        break