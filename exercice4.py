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
        print(f"{r}")
    return 

# Récuperer la date à laquelle le moins de vente a été enregistré
date_peu_vente = "SELECT COUNT (idBoisson), date FROM Ventes\
    GROUP BY date \
        ORDER BY COUNT(idBoisson)\
            LIMIT 1"
print("date_peu_vente =")
affiche(date_peu_vente)

# Récuperer la date à laquelle les bénéfices ont été les moins importants
date_peu_benefice = "SELECT ROUND(SUM(prix_EU),2), date AS benefice \
    FROM Ventes AS V, Carte AS C\
        WHERE C.idBoisson = V.idBoisson\
            GROUP BY date\
            ORDER BY benefice\
                LIMIT 1"
print("date_peu_benefice = ")
affiche(date_peu_benefice)

bdd.close()