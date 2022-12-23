#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv
from datetime import datetime

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

# pour l'exercice, on affiche les identifiants de connexion des managers
curseur.execute("SELECT * FROM Managers")
results = curseur.fetchall()
for r in results :
    print(r)


# Le manager se connecte
identifiant = input("\nEntrez votre identifiant : ")
mot_de_passe = input("Entrez votre matricule : ")

connexion = f"SELECT identifiant \
                FROM Managers \
                WHERE identifiant = '{identifiant}' \
                AND matricule = '{mot_de_passe}';"
curseur.execute(connexion)
if not curseur.fetchone() :  
    print("\nIdentifiants incorrects. Vous n'avez peut-être pas accès aux informations suivantes.")
    exit() 
else :
    print("\nBienvenue.")


# On sélectionne le bar du manager
curseur.execute(f"SELECT nom_bar \
                    FROM Etablissements \
                    WHERE matricule_manager = '{mot_de_passe}'")
nom_bar = curseur.fetchone()
print(f"\nVous êtes le manager du bar \"{nom_bar[0]}\".")


# Le manager tape le mois de son choix en chiffre. 
# On vérifie en même temps que c'est au bon format "mm"
# Le manager a droit à deux essais
mois = input("\nVous souhaitez les informations du mois de (au format mm) : ")
liste_mois = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
if mois not in liste_mois :
    mois = input("\nVous n'avez pas correctement rentrer le mois, veuillez recommencer (exemple pour le mois de janvier, taper 01) : ")
    if mois not in liste_mois :
        print("\nVous n'avez toujours pas correctement rentrer le mois. Le script se termine ici.")
        exit()

# Le manager tape l'annee de son choix en chiffre.
# pas de vérification car pas d'ambiguité comme avec le mois
annee = input("\nVous souhaitez les informations de l'annee (au format yyyy) : ")

date = f"/{mois}/{annee}"

# afficher le nombre de ventes effectuées ce mois-ci par ses employés et le montant que cela représente
boissons_vendues = 0 # nombre de ventes effectuées le mois sélectionné par le manager
recettes = 0 # les recettes de ses ventes
# on groupe par journée le nombre de boissons vendues et les recettes
curseur.execute(f"SELECT V.date, COUNT(V.idBoisson), ROUND(SUM(C.prix_EU), 2) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY V.date")
results = curseur.fetchall()
for r in results :
    if r[0].find(f"{date}") != -1 : # si dans la date dd/mm/yyyy, /mm/ = date = /mois/, soit le mois rentré par le manager
        boissons_vendues += r[1] # on fait la somme des boissons vendues chaque jour
        recettes += r[2] # on fait la somme des recettes journalières

if boissons_vendues == 0 : # s'il n'y a pas de données pour le mois selectionné, soit pas de boissons vendues, alors le script s'arrête
    print("\nIl n'y a pas de données pour ce mois-ci dans la base de données.")
    exit()
else :
    print(f"\nVos employés ont vendu {boissons_vendues} boissons pour un total de {recettes} euros.") # et le script continue


# afficher les bénéfices générés par chaque employé du bar.
print("\nVoici les bénéfices générés par chaque employé du bar.")
recettes_employe = 0 # on initialise la variable des bénéfices de l'employé
nom_employe = "" # on initialise une variable qui contiendra le prenom et le nom de l'employe
curseur.execute(f"SELECT V.date, E.nom, E.prenom, ROUND(SUM(C.prix_EU), 2) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY V.matricule, V.date")
results = curseur.fetchall()
for r in results :
    if r[0].find(f"{date}") != -1 : 
        nom = f"{r[2]} {r[1]}"
        if nom_employe != nom and len(nom_employe) != 0 :
            print(f"{nom_employe} a fait un bénéfice de {round(recettes_employe, 2)} euros.")
            nom_employe = nom
            recettes_employe = 0
        recettes_employe += r[3]
        nom_employe = f"{r[2]} {r[1]}"
print(f"{nom_employe} a fait un bénéfice de {round(recettes_employe, 2)} euros.")


bdd.close()
