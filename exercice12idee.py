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


# On attache les 6 requêtes suivantes à des variables

# affiche la boisson qui a rapporté le moins d'argent à la boisson qui a rapporté le plus d'argent
moins_bénéfice = f"SELECT C.boisson, ROUND(SUM(C.prix_EU), 2) \
                    FROM Employes AS E \
                    INNER JOIN Ventes AS V \
                    ON E.matricule = V.matricule \
                    INNER JOIN Carte AS C \
                    ON C.idBoisson = V.idBoisson \
                    WHERE E.nom_bar = \"{nom_bar[0]}\" \
                    GROUP BY C.boisson \
                    ORDER BY ROUND(SUM(C.prix_EU), 2)"

# affiche le bénéfice moyen d'une boisson
moyenne_bénéfice = f"SELECT ROUND(AVG(bénéfice), 2) \
                        FROM (SELECT SUM(C.prix_EU) AS bénéfice \
                                FROM Employes AS E \
                                INNER JOIN Ventes AS V \
                                ON E.matricule = V.matricule \
                                INNER JOIN Carte AS C \
                                ON C.idBoisson = V.idBoisson \
                                WHERE E.nom_bar = \"{nom_bar[0]}\" \
                                GROUP BY C.boisson \
                                ORDER BY ROUND(SUM(C.prix_EU), 2))"

# affiche le total des bénéfices
total_bénéfice = f"SELECT ROUND(SUM(C.prix_EU), 2) \
                    FROM Employes AS E \
                    INNER JOIN Ventes AS V \
                    ON E.matricule = V.matricule \
                    INNER JOIN Carte AS C \
                    ON C.idBoisson = V.idBoisson \
                    WHERE E.nom_bar = \"{nom_bar[0]}\""


# affiche la boisson la moins vendue à la boisson la plus vendue
moins_vendue = f"SELECT C.boisson, COUNT(V.idboisson) \
                    FROM Employes AS E \
                    INNER JOIN Ventes AS V \
                    ON E.matricule = V.matricule \
                    INNER JOIN Carte AS C \
                    ON C.idBoisson = V.idBoisson \
                    WHERE E.nom_bar = \"{nom_bar[0]}\" \
                    GROUP BY C.boisson \
                    ORDER BY COUNT(V.idboisson)"

# affiche le nombre de fois qu'a été vendue une boisson en moyenne
moyenne_vendue = f"SELECT ROUND(AVG(vendue), 2) \
                    FROM (SELECT COUNT(V.idboisson) AS vendue \
                    FROM Employes AS E \
                    INNER JOIN Ventes AS V \
                    ON E.matricule = V.matricule \
                    INNER JOIN Carte AS C \
                    ON C.idBoisson = V.idBoisson \
                    WHERE E.nom_bar = \"{nom_bar[0]}\" \
                    GROUP BY C.boisson \
                    ORDER BY COUNT(V.idboisson))"

# nombre total de boissons vendues
total_vendue = f"SELECT COUNT(V.idBoisson) \
                    FROM Employes AS E \
                    INNER JOIN Ventes AS V \
                    ON E.matricule = V.matricule \
                    INNER JOIN Carte AS C \
                    ON C.idBoisson = V.idBoisson \
                    WHERE E.nom_bar = \"{nom_bar[0]}\""

# On rattache les résultats à la variable de la requête car nous n'en avons plus besoin
curseur.execute(moyenne_bénéfice)
results = curseur.fetchall()
for r in results :
    moyenne_bénéfice = r[0]
    print(f"\nUne boisson a fait un bénéfice moyen de {moyenne_bénéfice} euros.")

curseur.execute(total_bénéfice)
results = curseur.fetchall()
for r in results :
    total_bénéfice = r[0]
    print(f"\nIl y a eu {total_bénéfice} euros de bénéfice total.")  

curseur.execute(moyenne_vendue)
results = curseur.fetchall()
for r in results :
    moyenne_vendue = r[0]
    print(f"\nune boisson a été vendue {moyenne_vendue} fois en moyenne.")

curseur.execute(total_vendue)
results = curseur.fetchall()
for r in results :
    total_vendue = r[0]
    print(f"\nIl y a eu {total_vendue} boissons vendues.")


# On affiche la liste des boissons en fonction de leur bénéfice et du nombre de fois qu'elles ont été vendues
print("\nbénéfice par boisson : ")
curseur.execute(moins_bénéfice)
results = curseur.fetchall()
for r in results :
    print(f"{r[0]} : {r[1]} euros")

print("\nnombre de vente par boisson : ")
curseur.execute(moins_vendue)
results = curseur.fetchall()
for r in results :
    print(f"{r[0]} : vendue {r[1]} fois.")