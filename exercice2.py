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


# les managers de bars
# filtre : les matricules des managers se trouvent à la fois dans la table Employes et Etablissements
# et les matricules des employés se trouvent uniquement dans la table Employes
curseur.execute("SELECT prenom, nom, E.nom_bar \
                FROM Employes as E, Etablissements as T \
                WHERE E.matricule = T.matricule_manager \
                AND E.nom_bar = T.nom_bar")
print("\nliste des managers de bars : ")
results = curseur.fetchall()
for r in results:
    print(f"{r[1]} {r[0]} dirige le bar \"{r[2]}\".")

# nombre d'employés pour chaque profession
# regroupement et calcul : on regroupe le comptage des employés (grâce à leur matricule) par profession
curseur.execute("SELECT COUNT(matricule), profession \
                    FROM Employes GROUP BY profession")
print("\nnombre d'employés pour chaque profession : ")
results = curseur.fetchall()
for r in results:
    print(f"{r[0]} {r[1]}s")

# revenu total du groupe
# calcul : grâce à la jointure entre les tables Ventes et Cartes, chaque vente (ligne du tableau) a le prix de la boisson indiqué
# on fait la somme des prix des boissons, on arrondie le résultat à deux chiffres après la virgule (au centime près)
curseur.execute("SELECT ROUND(SUM(Carte.prix_EU), 2) \
                FROM Ventes, Carte \
                WHERE Ventes.idBoisson = Carte.idBoisson")
print("\nrevenu total du groupe : ")
results = curseur.fetchall()
for r in results:
    print(f"Les revenus du groupe sont de {r[0]} euros.")

bdd.close()
