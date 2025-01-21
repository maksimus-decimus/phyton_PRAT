from ast import Index


class Cola_LIFO:
    def __init__(self):
        """
        Constructor de la classe.
        Inicialitza una llista buida per la pila.
        """
        self.elements = []

    def afegir(self, element):
        """
        Afegeix un element a la part superior de la pila.

        Paràmetres:
        - element: qualsevol tipus d'element.
        """
        self.elements.append(element)
    def extreure(self):
        """
        Extreu i retorna l'últim element afegit (part superior de la pila).
        Llença un error si la pila està buida.
        """
        if self.buit():
            raise IndexError("Pila buida, no es pot extreure")
        return self.elements.pop()

    def veure_darrer(self):
        """
        Retorna l'últim element afegit sense extreure'l.
        Llença un error si la pila està buida.
        """
        if self.buit():
            raise IndexError("No hi ha cap element")
        return self.elements[-1]

    def buit(self):
        """
        Retorna True si la pila està buida, False en cas contrari.
        """
        return len(self.elements) == 0

    def longitud(self):
        """
        Retorna el nombre d'elements de la pila.
        """
        return len(self.elements)


pila = Cola_LIFO()
pila.afegir("A")
pila.afegir("B")
pila.afegir("C")

print(pila.veure_darrer())  # Sortida: "C" (últim element afegit)
print(pila.extreure())  # Sortida: "C"
print(pila.veure_darrer())  # Sortida: "B"
print(pila.longitud())  # Sortida: 2
print(pila.buit())  # Sortida: False
pila.extreure()
pila.extreure()
print(pila.buit()) #Sortida: True 
