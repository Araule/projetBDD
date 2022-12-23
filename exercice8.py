#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

#connexion du manager
identifiant = input("\nEntrez votre identifiant : ")
mot_de_passe = input("Entrez votre matricule : ")

connexion = f"SELECT identifiant \
                FROM Managers \
                WHERE identifiant = '{identifiant}' \
                AND matricule = '{mot_de_passe}';"
curseur.execute(connexion)
if not curseur.fetchone() :  
    print("\nIdentifiants incorrects.")
    exit() 
else :
    print("\nVous souhaitez connaître le nombre de boissons vendues dans votre établissement.\n")

curseur.execute(f"SELECT nom_bar \
                    FROM Etablissements \
                    WHERE matricule_manager = '{mot_de_passe}'")
nom_bar = curseur.fetchone()

print(f"Vous êtes le manager du bar \"{nom_bar[0]}\".\n")


#problèmes : 
#faire entrer que le mois à l'utilisateur
#faire apparaître les employés ayant vendus le moins de boissons dans la même requête

curseur.execute(f"SELECT C.boisson, COUNT(V.idBoisson)\
    FROM Carte AS C, Ventes AS V, Etablissements AS Et, Employes AS E\
        WHERE C.idBoisson = V.idBoisson\
            AND V.date BETWEEN '01-11-2022' AND '31-11-2022'\
                AND V.matricule = E.matricule\
                    AND E.nom_bar =\"{nom_bar[0]}\"\
                        AND Et.nom_bar = \"{nom_bar[0]}\"\
                        GROUP BY C.boisson\
                        ORDER BY COUNT(V.idBoisson)\
                            LIMIT 10") #affiche les 10 boissons les moins vendues

results = curseur.fetchall()
for r in results :
    print(f"{r[0]} n'a été vendu que {r[1]} fois.")

bdd.close()
