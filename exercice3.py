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

#boissons vendues par chaque employé
#problème rencontré : sqlite3.OperationalError: ambiguous column name:idBoisson
#explication : même attribut dans deux tables différentes (Ventes, Carte)
#solution : mettre le nom de la table comme préfixe à l'attribut pour savoir indiquer l'attribut de la table qu'on souhaite
nb_boissons_employes = "SELECT Ventes.matricule, COUNT(Ventes.idBoisson), ROUND(SUM(Carte.prix_EU),2) \
                            FROM Ventes, Carte \
                            WHERE Carte.idBoisson = Ventes.idBoisson \
                            GROUP BY Ventes.matricule"
print("\nnombre de boissons vendues par chaque employé : ")
print("(matricule de l'employé, nombre de boissons vendues par l'employé, revenu total de la vente de ses boissons (en euro))")
affiche(nb_boissons_employes)

bdd.close()


