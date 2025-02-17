#Videojoc Python (Amb classes i mètodes)
import random
from time import sleep


class Personatje:
    def __init__(self, nom, vida, atac, defensa, experiencia):
        self.nom = nom
        self.vida = vida
        self.atac = atac
        self.defensa = defensa
        self.experiencia = experiencia


    def esta_viu(self):
        return self.vida > 0        #Si la vida és superior a 0


    def rebre_dany(self, dany):
        self.vida = max(0, dany - self.defensa )    #A la vida se li resta el dany menys la defensa


    def atacar(self, altre_personatge):
        dany = random.randint(0, self.atac)
        print(f"{self.nom} ataca a {altre_personatge.nom} y causa {dany} de dany")
        altre_personatge.rebre_dany(dany)

        if (self.expriencia > 0):
            self.defensa = self.defensa * 1.1
            self.atac = self.atac * 1.1

    def recalcular_atac_defensa(self):
        if self.experiencia > 0:
            self.atac = self.atac * 1 +(0.1 * self.experiencia) * self.atac
            self.defensa = self.defensa * 1 +(0.1 * self.experiencia) * self.defensa


    def estadistiques(self):
        return (f"{self.nom} té salud:{self.vida}, atac:{self.atac}, defensa:{self.defensa}")


class Joc:
    def __init__(self, personatge1, personatge2):
        self.personatge1 = personatge1
        self.personatge2 = personatge2

    def combat(self):
        while self.personatge1.esta_viu() and self.personatge2.esta_viu():
            print(f"{self.personatge1.nom} ataca a {self.personatge2.nom}")
            self.personatge1.atacar(self.personatge2)
            self.versus()
            print(f"{self.personatge2.nom} ataca a {self.personatge1.nom}")
            self.personatge2.atacar(self.personatge1)
            self.versus()

        if self.personatge1.esta_viu():
            self.personatge1.experiencia = self.personatge1.experiencia + 1
            self.personatge1.recalcular_atac_defensa()
            print(f"{self.personatge1.nom} ha guanyat")
            self.personatge1.estadistiques()

        else:
            self.personatge2.experiencia = self.personatge2.experiencia + 1
            self.personatge2.recalcular_atac_defensa()
            print(f"{self.personatge2.nom} ha guanyat")
            self.personatge2.estadistiques()


    def versus(self):
        print(f"    {self.personatge1.nom}       {self.personatge2.nom}")
        print(f"vida:{self.personatge1.vida}       {self.personatge2.vida}")
        print()


p1=Personatje("p1", 100, 100, 2)
p2=Personatje("p2", 100,12,3)

joc1=Joc(p1,p2)
joc1.combat()
joc1.personatge2.experiencia