import heapq

class Documento:
    def __init__(self, nombre, prioridad):
        self.heap = []
        self.contador = 0

        self.nombre = nombre
        self.prioridad = prioridad


def añadir_documento(self):
    nombre = input("Ingrese el nombre del documento")
    prioridad = int(input("Añada la prioridad"))
    documento = Documento(nombre,prioridad)
    heapq.heappush(self.heap, documento, self.contador)
    self.contador += 1
    print (f"Documento '{nombre}' añadido a la cola")

def imprimir_trabajo(self):
    documento = heapq.heappop(self.cola)
    print(f"Imprimiendo el documento: {documento.nombre} con prioridad: {documento.prioridad}")




while True:
    print("\n1. Añadir documento")
    print("2. Imprimir trabajo")

    opcion = input("Seleccione la opción que desea: ")

    if opcion == "1":
        Documento.añadir_documento()
    elif opcion =="2":
        Documento.imprimir_trabajo()
    else:
        print("No válida")
        opcion = input("Seleccione de nuevo la opción: ")
