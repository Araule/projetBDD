#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

# boissons vendues par chaque employé et le montant total associé à ces ventes
# regroupement : on regroupe par employé grâce à leur matricule
# calcul : on compte le nombre de boissons vendus en comptant le nombre de ventes effectués (chaque vente reçoit un id unique)
# Grâce à la jointure entre les tables Ventes et Cartes, chaque vente (ligne du tableau) a le prix de la boisson indiqué
# on fait la somme des prix des boissons, on arrondie le résultat à deux chiffres après la virgule (au centime près)
curseur.execute("SELECT E.nom, E.prenom, COUNT(V.idBoisson), ROUND(SUM(C.prix_EU),2) \
                    FROM Ventes AS V, Carte AS C, Employes AS E \
                    WHERE C.idBoisson = V.idBoisson \
                    AND E.matricule = V.matricule \
                    GROUP BY V.matricule")
print("\nnombre de boissons vendues par chaque employé : ")
results = curseur.fetchall()
for r in results:
    print(f"{r[1]} {r[0]} a vendu {r[2]} boissons pour un total de {r[3]} euros.")

bdd.close()


