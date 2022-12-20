#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

def affiche(requete):
    curseur.execute(requete)
    results = curseur.fetchall()
    for r in results:
        print(r)
    return 

# nombre total de bars
nb_bars = "SELECT COUNT(nom_bar) \
            FROM Etablissements"
print("\nnombre total de bars : ")
affiche(nb_bars)

# nombre total d'employés
nb_employes = "SELECT COUNT(matricule) \
                FROM Employes"
print("\nnombre total d'employés : ")
affiche(nb_employes)

#les managers de bars
manager_bar = "SELECT prenom, nom, E.nom_bar \
                FROM Employes as E, Etablissements as T \
                WHERE E.matricule = T.matricule_manager \
                AND E.nom_bar = T.nom_bar"
print("\nliste des managers de bars : ")
print("(Nom, Prénom, Nom du bar)")
affiche(manager_bar)

#nombre d'employés pour chaque profession
nb_employes_prof = "SELECT COUNT(matricule), profession \
                    FROM Employes GROUP BY profession"
print("\nnombre d'employés pour chaque profession : ")
print("(Nombre d'employé d'une profession, Nom de la profession)")
affiche(nb_employes_prof)

#revenu total du groupe
#Revu par Camille, fonctionne.
#problème rencontré avec COUNT(idBoisson) : sqlite3.OperationalError: ambiguous column name:idBoisson
#explication : même attribut dans deux tables différentes (Ventes, Carte)
#solution : mettre le nom de la table comme préfixe à l'attribut pour savoir quel attribut on souhaite
revenu_total = "SELECT COUNT(Ventes.idBoisson), ROUND(SUM(Carte.prix_EU),2) \
                FROM Ventes, Carte \
                WHERE Ventes.idBoisson = Carte.idBoisson"
print("\nrevenu total du groupe : ")
print("(Nombre de boissons vendues, revenu total sur la vente des boissons(en euro))")
affiche(revenu_total)

bdd.close()
