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
nb_bars = "SELECT COUNT(NAME) FROM Etablissements"
affiche(nb_bars)

# nombre total d'employés
nb_employes = curseur.execute("SELECT COUNT(matricule) FROM Employes")
affiche(nb_employes)

#les managers de bars
manager_bar = curseur.execute("SELECT prenom, nom, nom_bar FROM Employes as E, Etablissements as T WHERE E.matricule = T.matricule_manager")
affiche(manager_bar)

#nombre d'employés pour chaque profession
nb_employes_prof = curseur.execute("SELECT COUNT(matricule), profession FROM Employes GROUP BY profession")
affiche(nb_employes_prof)

#revenu total du groupe
revenu_total = curseur.execute("SELECT SUM(prix) FROM Carte as C INNER JOIN Ventes as V ON C.idBoisson = V.idBoisson")
affiche(revenu_total)

bdd.close()