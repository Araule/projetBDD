#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv

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


# afficher les employés qui ont vendu le plus de cocktails du jour et de bières en pression
# filtre : nom du bar du manager connecté
# filtre 2 : nom de la boisson : "Cocktail du moment" ou "Blonde pression"
# regroupement : par employé, grâce à leur matricule
# trie : le nombre de boissons vendues par chaque employé, du nombre le plus grand au plus petit
# limite : on limite la recherche à 5 résultats
print("\nVoici la liste des 5 employés qui ont vendu le plus de cocktails du jour et de bières en pression.")
curseur.execute(f"SELECT E.nom, E.prenom, COUNT(V.idBoisson) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            AND boisson = \"Cocktail du moment\" \
            OR boisson = \"Blonde pression\" \
            GROUP BY V.matricule \
            ORDER BY COUNT(V.idBoisson) DESC \
            LIMIT 5")
results = curseur.fetchall()
for r in results :
    print(f"{r[1]} {r[0]} a vendu {r[2]} cocktails du jour et bières en pression.")