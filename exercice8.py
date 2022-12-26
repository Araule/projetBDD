#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv
from datetime import datetime

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

# pour l'exercice, on affiche les identifiants de connexion des managers
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


# afficher les boissons les moins vendues dans l’établissement ce mois-ci
# filtre : le nom du bar du manager connecté
# regroupement : grâce au jointure entre Carte et Ventes, les ventes sont regroupés par le nom de boisson de la table Carte
# trie : par le nombre de boisson vendu (selon leur nom), du nombre le plus petit au plus grand
# limite : on limite la recherche à 10 résultats
print("\nVoici la liste des 10 boissons qui se sont le moins bien vendues dans votre établissement au mois de Novembre.")
curseur.execute(f"SELECT C.boisson, COUNT(V.idBoisson) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY C.boisson \
            ORDER BY COUNT(V.idBoisson) \
            LIMIT 10")
results = curseur.fetchall()
for r in results :
    print(f"{r[0]} n'a été vendu que {r[1]} fois.")


# afficher les employés ayant vendu le moins de boissons.
# filtre : le nom du bar du manager connecté
# regroupement : grâce au jointure entre Employes et Ventes, les ventes sont regroupés par employés
# trie : par le nombre de boisson vendu (selon l'employé), du nombre le plus petit au plus grand
# limite : on limite la recherche à 5 résultats
print("\nVoici la liste des 5 employés qui ont vendu le moins de boissons au mois de Novembre.")
curseur.execute(f"SELECT E.nom, E.prenom, COUNT(V.idBoisson) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY V.matricule \
            ORDER BY COUNT(V.idBoisson) \
            LIMIT 5")
results = curseur.fetchall()
for r in results :
    print(f"{r[1]} {r[0]} n'a vendu que {r[2]} boissons.")


bdd.close()
