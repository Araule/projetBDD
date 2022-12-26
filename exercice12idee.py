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
mot_de_passe = input("Entrez votre mmot de passe : ")
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


# On sélectionne le bar du manager pour filtrer les requêtes qui suivent
curseur.execute(f"SELECT nom_bar \
                    FROM Etablissements \
                    WHERE matricule_manager = '{mot_de_passe}'")
nom_bar = curseur.fetchone()
print(f"\nVous êtes le manager du bar \"{nom_bar[0]}\".")


# On rattache les résultats des deux requêtes à une variable pour les réutiliser plus tard
curseur.execute(f"SELECT ROUND(SUM(C.prix_EU), 2) \
                    FROM Employes AS E \
                    INNER JOIN Ventes AS V \
                    ON E.matricule = V.matricule \
                    INNER JOIN Carte AS C \
                    ON C.idBoisson = V.idBoisson \
                    WHERE E.nom_bar = \"{nom_bar[0]}\"") # total des bénéfices du mois de novembre dans le bar du manager
results = curseur.fetchall()
for r in results :
    total_bénéfice = r[0]

curseur.execute(f"SELECT COUNT(V.idBoisson) \
                    FROM Employes AS E \
                    INNER JOIN Ventes AS V \
                    ON E.matricule = V.matricule \
                    INNER JOIN Carte AS C \
                    ON C.idBoisson = V.idBoisson \
                    WHERE E.nom_bar = \"{nom_bar[0]}\"") # nombre total de boissons vendues au mois de novembre dans le bar du manager
results = curseur.fetchall()
for r in results :
    total_vendue = r[0]


# On crée une liste vide qui contiendra le nom des boissons que le manager peut supprimer de la carte
liste_boisson = []
# Si une boisson représente moins de 1% des bénéfices du bar et 1% du nombre des boissons vendus par le bar
# Alors le manager peut l'enlever de la carte


# affiche la boisson qui a rapporté le moins d'argent à la boisson qui a rapporté le plus d'argent
i = 0 # on initialise un compteur
curseur.execute(f"SELECT C.boisson, ROUND(SUM(C.prix_EU), 2) \
                    FROM Employes AS E \
                    INNER JOIN Ventes AS V \
                    ON E.matricule = V.matricule \
                    INNER JOIN Carte AS C \
                    ON C.idBoisson = V.idBoisson \
                    WHERE E.nom_bar = \"{nom_bar[0]}\" \
                    GROUP BY C.boisson \
                    ORDER BY ROUND(SUM(C.prix_EU), 2)")
results = curseur.fetchall()
for r in results :
    if r[1] < (total_bénéfice * 0.01) :
        curseur.execute(f"SELECT COUNT(V.idboisson) \
                            FROM Employes AS E \
                            INNER JOIN Ventes AS V \
                            ON E.matricule = V.matricule \
                            INNER JOIN Carte AS C \
                            ON C.idBoisson = V.idBoisson \
                            WHERE E.nom_bar = \"{nom_bar[0]}\" \
                            AND C.boisson = \"{r[0]}\"")
        results2 = curseur.fetchall()
        for r2 in results2 :
            if r2[0] < (total_vendue * 0.01) :
                liste_boisson.append(f"{r[0]} : {r[1]} euros de bénéfice, vendue {r2[0]} fois")
                i += 1

print(f"\nVous pouvez supprimer de la carte {i} boissons.")
for ligne in liste_boisson :
    print(ligne)

bdd.close()