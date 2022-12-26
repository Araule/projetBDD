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


# afficher quel degré d’alcool moyen est consommé dans son établissement et quelle quantité d’alcool a été vendue ce mois-ci
# filtre : nom du bar selon le manager connecté
curseur.execute(f"SELECT COUNT(V.idBoisson), ROUND(AVG(C.degre_BIERES), 2), SUM(C.quantite_CL) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\"")
results = curseur.fetchall()
for r in results :
    print(f"\nAu mois de Novembre, {r[0]} boissons ont été vendu pour un total de {r[2]} CL d'alcools. Le degré moyen d'alcool consommé, dans le cas des bières vendues, était de {r[1]} %.")