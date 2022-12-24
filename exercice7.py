#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv

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


# Le manager choisit une date.
date_saisie = input("\nTaper la  date de votre choix (au format jj/11/2022) : ")


# afficher le nombre de ventes effectuées par ses employés et le montant que cela représente à la date choisie
curseur.execute(f"SELECT COUNT(V.idBoisson), ROUND(SUM(C.prix_EU), 2) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            AND V.date = \"{date_saisie}\" \
            GROUP BY V.date")
results = curseur.fetchall()
if not results :  # s'il n'y a pas de résultat
    print("\nNous n'avons pas de données pour cette journée. Peut-être n'avez-vous pas correctement saisi la date de votre choix.")
    exit()
for r in results : # sinon
    print(f"\nLe {date_saisie}, vos employés ont vendu {r[0]} boissons pour un total de {r[1]} euros.")


# afficher les bénéfices générés par chaque employé du bar à la date choisie.
print(f"\nVoici les bénéfices générés par chacun de vos employés le {date_saisie}.")
curseur.execute(f"SELECT E.nom, E.prenom, ROUND(SUM(C.prix_EU), 2) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            AND V.date = \"{date_saisie}\" \
            GROUP BY V.matricule")
results = curseur.fetchall()
if not results :  # s'il n'y a pas de résultat
    print("\nNous n'avons pas de données pour cette journée. Peut-être n'avez-vous pas correctement saisi la date de votre choix.")
    exit()
for r in results : # sinon
    print(f"{r[1]} {r[0]} a fait un bénéfice de {round(r[2], 2)} euros.")


bdd.close()
