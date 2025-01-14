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


print (calcular_total(comandes, "Marta"))
print ()

def clients_comanda_minim(comandes, minim_import): ## 2.
    clients = []
    for client, llista_comandes in comandes.items():
        total = sum(quantitat * preu for _, quantitat, preu in llista_comandes)
        if total > minim_import:
            clients.append(client)
    print("El client que ha gastat més de 100 euros es:")
    return clients


print(clients_comanda_minim(comandes,100))
print()

def imprimir_comandas_totes(comandes,client):## 3.
    if client in comandes:
        print(f"El client {client}:")
        for producte, quantitat, preu in comandes[client]:
            print(f"Ha comprat - {producte}: {quantitat} unitats a {preu} €")


imprimir_comandas_totes(comandes,"Anna")

