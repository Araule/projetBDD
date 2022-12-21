#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()


# nombre total de bars
curseur.execute("SELECT COUNT(nom_bar) \
                FROM Etablissements")
results = curseur.fetchall()
for r in results:
    print(f"\nnombre total de bars : {r[0]}")

# nombre total d'employés
curseur.execute("SELECT COUNT(matricule) \
                FROM Employes")
results = curseur.fetchall()
for r in results:
    print(f"\nnombre total d'employés : {r[0]}")

#les managers de bars
curseur.execute("SELECT prenom, nom, E.nom_bar \
                FROM Employes as E, Etablissements as T \
                WHERE E.matricule = T.matricule_manager \
                AND E.nom_bar = T.nom_bar")
print("\nliste des managers de bars : ")
results = curseur.fetchall()
for r in results:
    print(f"{r[1]} {r[0]} dirige le bar \"{r[2]}\".")

#nombre d'employés pour chaque profession
curseur.execute("SELECT COUNT(matricule), profession \
                    FROM Employes GROUP BY profession")
print("\nnombre d'employés pour chaque profession : ")
results = curseur.fetchall()
for r in results:
    print(f"{r[0]} {r[1]}s")

#revenu total du groupe
#Revu par Camille, fonctionne.
#problème rencontré avec COUNT(idBoisson) : sqlite3.OperationalError: ambiguous column name:idBoisson
#explication : même attribut dans deux tables différentes (Ventes, Carte)
#solution : mettre le nom de la table comme préfixe à l'attribut pour savoir quel attribut on souhaite
curseur.execute("SELECT COUNT(Ventes.idBoisson), ROUND(SUM(Carte.prix_EU), 2) \
                FROM Ventes, Carte \
                WHERE Ventes.idBoisson = Carte.idBoisson")
print("\nrevenu total du groupe : ")
results = curseur.fetchall()
for r in results:
    print(f"{r[0]} boissons ont été vendues, pour un total de {r[1]} euros.")

bdd.close()
