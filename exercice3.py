#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

#boissons vendues par chaque employé
#problème rencontré : sqlite3.OperationalError: ambiguous column name:idBoisson
#explication : même attribut dans deux tables différentes (Ventes, Carte)
#solution : mettre le nom de la table comme préfixe à l'attribut pour savoir indiquer l'attribut de la table qu'on souhaite
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


