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

# Récuperer la date à laquelle le moins de vente a été enregistré
curseur.execute("SELECT COUNT (idBoisson), date FROM Ventes \
                    GROUP BY date \
                    ORDER BY COUNT(idBoisson) \
                    LIMIT 1")
print("\nla date à laquelle le moins de vente a été enregistré : ")
results = curseur.fetchall()
for r in results :
    print(f"Le {r[1]} a été vendu seulement {r[0]} boissons.")

# Récuperer la date à laquelle les bénéfices ont été les moins importants
curseur.execute("SELECT ROUND(SUM(prix_EU),2), date AS benefice \
                        FROM Ventes AS V, Carte AS C \
                        WHERE C.idBoisson = V.idBoisson \
                        GROUP BY date \
                        ORDER BY benefice \
                        LIMIT 1")
print("\nla date à laquelle les bénéfices ont été les moins importants : ")
results = curseur.fetchall()
for r in results :
    print(f"Le {r[1]} a été fait un bénéfice de seulement {r[0]} euros.")

bdd.close()