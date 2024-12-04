class Projecte:
    def __init__(self, nom, duracio,llenguatge):

        self.nom = nom
        self.duracio = duracio
        self.llenguatge = llenguatge
        self.tasques = []
        self.equips = []

    def mostrar_informacio(self):
        return  (f"PROJECTE: {self.nom}, DURADA: {self.duracio} mesos de temps, LLENGUATGE: {self.llenguatge}")


    def afegir_tasca(self, tasca):
        self.tasques.append(tasca)

    def mostrar_tasques(self):
        tasques_informacio = " "
        for tasca in self.tasques:
            tasques_informacio += f" -> TASCA: {tasca.titol} ESTAT: {tasca.estat} RESPONSABLE: {tasca.membre.nom}\n"
        return tasques_informacio


class ProjecteIntern(Projecte):
    def __init__(self, nom, duracio,llenguatge,responsable,departament):
        super().__init__(nom, duracio,llenguatge)
        self.responsable = responsable
        self.departament = departament

    def mostrar_informacio(self):
        info = super().mostrar_informacio()
        info += f", Responsable: {self.responsable}, Departament: {self.departament}"
        return info



class ProjecteExtern(Projecte):
    def __init__(self, nom, duracio, llenguatge,client,pressupost):
        super().__init__(nom, duracio, llenguatge)
        self.client = client
        self. pressupost = pressupost

    def mostrar_informacio(self):
        info = super().mostrar_informacio()
        info += f", Client: {self.client}, Pressupost: {self.pressupost}K€"
        return info


class Equip:
    def __init__(self,nomEquip):
        self.nomEquip = nomEquip
        self.membres = []

    def afegir_membre(self, membre):
        self.membres.append(membre)

    def mostrar_membres(self):
        info_membres = (f" ")
        for membre in self.membres:
            info_membres += f" -> Nom del MEMBRE: {membre.nom} ROL: {membre.rol}, {membre.experiencia} anys d'experiència\n"
        return info_membres

    def mostrar_informacio(self):
        return (f"{self.nomEquip}, Membres: {len(self.membres)}") #"len" funciona per llegir el length de una variable, com hi han 2 membres definits, surt que [0] i [1] son 2 valors


class Membre:
    def __init__(self, nom,rol,experiencia):
        self.nom = nom
        self.rol = rol
        self.experiencia = experiencia

    def mostrar_membre(self):
        return self.nom

class Tasca:
    def __init__(self,titol,estat,membre):

        self.titol = titol
        self.estat = estat
        self.membre = membre




if __name__ == "__main__":
    # Crear un projecte intern
    projecte_intern = ProjecteIntern(
        nom="Aplicació CRM Interna",
        duracio=12,
        llenguatge="Python",
        responsable="Joan Rovira",
        departament="IT"
    )

    # Crear un projecte extern
    projecte_extern = ProjecteExtern(
        nom="Plataforma E-learning",
        duracio=18,
        llenguatge="Java",
        client="Educorp",
        pressupost=300
    )

    # Crear un equip i membres
    equip = Equip("Equip Desenvolupament")
    membre1 = Membre("Anna", "Desenvolupadora", 3)
    membre2 = Membre("Marc", "Tester", 2)
    equip.afegir_membre(membre1)
    equip.afegir_membre(membre2)

    # Afegir tasques al projecte intern
    tasca1 = Tasca("Definir requeriments", "pendent", membre1)
    tasca2 = Tasca("Provar funcionalitats", "pendent", membre2)
    projecte_intern.afegir_tasca(tasca1)
    projecte_intern.afegir_tasca(tasca2)

    # Mostrar informació del projecte intern
    print("Informació del projecte intern:")
    print(projecte_intern.mostrar_informacio())
    print("\nTasques del projecte intern:")
    print(projecte_intern.mostrar_tasques())

    # Mostrar informació de l'equip
    print("\nInformació de l'equip:")
    print(equip.mostrar_informacio())
    print("\nMembres de l'equip:")
    print(equip.mostrar_membres())

    # Mostrar informació del projecte extern
    print("\nInformació del projecte extern:")
    print(projecte_extern.mostrar_informacio())


