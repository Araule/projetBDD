#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()


# Récuperer la date à laquelle le moins de vente a été enregistré
# regroupement : par date
# trie : par le nombre de boissons vendues par jour, du nombre le plus petit au plus grand
# limite : on limite la recherche à 1 seul résultat
curseur.execute("SELECT COUNT (idBoisson), date \
                    FROM Ventes \
                    GROUP BY date \
                    ORDER BY COUNT(idBoisson) \
                    LIMIT 1")
print("\nla date à laquelle le moins de vente a été enregistré : ")
results = curseur.fetchall()
for r in results :
    print(f"Le {r[1]} a été vendu seulement {r[0]} boissons.")

# Récuperer la date à laquelle les bénéfices ont été les moins importants
# regroupement : par date
# trie : par les revenus de la journée, du nombre le plus petit au plus grand
# limite : on limite la recherche à 1 seul résultat
curseur.execute("SELECT ROUND(SUM(prix_EU),2), date \
                        FROM Ventes AS V, Carte AS C \
                        WHERE C.idBoisson = V.idBoisson \
                        GROUP BY date \
                        ORDER BY ROUND(SUM(prix_EU),2) \
                        LIMIT 1")
print("\nla date à laquelle les bénéfices ont été les moins importants : ")
results = curseur.fetchall()
for r in results :
    print(f"Le {r[1]} a été fait un bénéfice de seulement {r[0]} euros.")

bdd.close()