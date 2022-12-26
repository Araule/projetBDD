#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv
from datetime import datetime

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

# on affiche les identifiants de connexion des managers
curseur.execute("SELECT * FROM Managers")
results = curseur.fetchall()
for r in results :
    print(r)


# Le manager se connecte
identifiant = input("\nEntrez votre identifiant : ")
mot_de_passe = input("Entrez votre matricule : ")
connexion = f"SELECT identifiant \
                FROM Managers \
                WHERE identifiant = '{identifiant}' \
                AND matricule = '{mot_de_passe}';"
curseur.execute(connexion)
if not curseur.fetchone() :  
    print("\nIdentifiants incorrects. Vous n'avez peut-être pas accès aux informations suivantes.")
    exit() 
else :
    print("\nBienvenue.")


# On sélectionne le bar du manager
curseur.execute(f"SELECT nom_bar \
                    FROM Etablissements \
                    WHERE matricule_manager = '{mot_de_passe}'")
nom_bar = curseur.fetchone()
print(f"\nVous êtes le manager du bar \"{nom_bar[0]}\".")


# afficher les boissons qui ont rapporté le plus d’argent dans leur établissement ce mois-ci
# filtre : nom du bar du manager connecté
# regroupement: par nom de boisson
# trie : la somme des ventes de chaque boisson, arrondie au centime près, du nombre le plus grand au plus petit
# limite : on limite la recherche au dix premiers résultats
print("\nVoici la liste des 10 boissons qui ont rapporté le plus d'argent au mois de Novembre.")
curseur.execute(f"SELECT C.boisson, ROUND(SUM(C.prix_EU), 2) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY C.boisson \
            ORDER BY ROUND(SUM(C.prix_EU), 2) DESC \
            LIMIT 10")
results = curseur.fetchall()
for r in results :
    print(f"{r[0]} a permis un bénéfice de {r[1]} euros.")


# afficher les employés ayant rapporté le plus d’argent.
# filtre : nom du bar du manager connecté
# regroupement: par employé, grâce à leur matricule
# trie : la somme des ventes effectuées par chaque employé, arrondie au centime près, du nombre le plus grand au plus petit
# limite : on limite la recherche au 5 premiers résultats
print("\nVoici la liste des 5 employés qui ont rapporté le plus d'argent au mois de Novembre.")
curseur.execute(f"SELECT E.nom, E.prenom, ROUND(SUM(C.prix_EU), 2) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY V.matricule \
            ORDER BY ROUND(SUM(C.prix_EU), 2) DESC \
            LIMIT 5")
results = curseur.fetchall()
for r in results :
    print(f"{r[1]} {r[0]} a fait un bénéfice de {r[2]} euros.")