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


# On sélectionne le bar du manager
curseur.execute(f"SELECT nom_bar \
                    FROM Etablissements \
                    WHERE matricule_manager = '{mot_de_passe}'")
nom_bar = curseur.fetchone()
print(f"\nVous êtes le manager du bar \"{nom_bar[0]}\".")


# afficher le nombre de ventes effectuées ce mois-ci par ses employés et le montant que cela représente
# filtre : nom du bar du manager connecté
# calcul : on refait le même calcul en comptant le nombre de boisson vendu, 
# et en faisant la somme du prix de chaque boisson vendue, arrondie au centime près
curseur.execute(f"SELECT COUNT(V.idBoisson), ROUND(SUM(C.prix_EU), 2) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\"")
results = curseur.fetchall()
for r in results :
    print(f"\nVos employés ont vendu {r[0]} boissons pour un total de {r[1]} euros en Novembre.")


# afficher les bénéfices générés par chaque employé du bar.
# filtre : nom du bar du manager connecté
# regroupement : par matricule, et par conséquent par employé, des ventes effectués par chacun d'entre eux
# calcul : pour chaque employé, on calcul la somme du prix des boissons vendues, arrondie au centime près
print("\nVoici les bénéfices générés par chacun de vos employés en Novembre.")
curseur.execute(f"SELECT E.nom, E.prenom, ROUND(SUM(C.prix_EU), 2) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY V.matricule")
results = curseur.fetchall()
for r in results :
    print(f"{r[1]} {r[0]} a fait un bénéfice de {round(r[2], 2)} euros.")


bdd.close()
