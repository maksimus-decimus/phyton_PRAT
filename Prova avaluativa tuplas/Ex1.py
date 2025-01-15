##BOTIGA

#BASE DONADA PEL DOCUMENT (nom_producte, quantitat, preu_unitari).


comandes = {
    "Anna": [("Llibre", 2, 10.0), ("Bolígraf", 5, 1.5)],
    "Joan": [("Carpeta", 3, 4.5)],
    "Marta": [("Ordinador", 1, 800.0), ("Ratolí", 2, 20.0)]
}

def calcular_total(comandes,client): ## 1.
    if client in comandes:
        total = sum(quantitat * preu for _, quantitat, preu in comandes[client]) ##si no posso "_" el programa em diu que hi han massa dades per compilar
        print("El total es:")
        return total




def clients_comanda_minim(comandes, minim_import): ## 2.
    clients = []
    for client, llista_comandes in comandes.items():
        total = sum(quantitat * preu for _, quantitat, preu in llista_comandes)
        if total > minim_import:
            clients.append(client)
    print("El client que ha gastat més de 100 euros es:")
    return clients




def imprimir_comandas_totes(comandes,client):## 3.
    if client in comandes:
        print(f"El client {client}:")
        for producte, quantitat, preu in comandes[client]:
            print(f"Ha comprat - {producte}: {quantitat} unitats a {preu} €")





while True:
    print('\033[H\033[J')
    print()
    print("Benvingut al programa de la botiga:")
    print()
    print("1. Veure cost total de cada client")
    print("2. Veure clients que han gastat més de 100 €")
    print("3. Veure de comandes d'un client")
    print("4. Sortir del programa")
    print()
    print("Escriu la teva selecció: ")
    seleccio = input()

    if seleccio == '1':
        while True:
            print("Escriu el nom del client: ")
            clientINTRO= input()


            if clientINTRO == "Marta" or clientINTRO == "Anna" or clientINTRO == "Joan":
                print(calcular_total(comandes, clientINTRO))
                input("Prem enter per continuar...")
                break


            else:
                print("No existeix!")
                continue

    elif seleccio == '2':
        print(clients_comanda_minim(comandes,100))
        input("Prem enter per continuar...")



    elif seleccio == '3':
        print("De quin client vols veure les comandes?")
        clientINTRO=input()
        print(imprimir_comandas_totes(comandes,clientINTRO))
        input("Prem enter per continuar...")


    elif seleccio =='4':
        print("Sortint del programa...")
        break


    else:
        print("Opció no vàlida! Escriu una vàlida: ")
        seleccio=input()