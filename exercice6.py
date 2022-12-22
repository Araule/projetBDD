#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

def affiche(requete):
    curseur.execute(requete)
    results = curseur.fetchall()
    for r in results:
        print(f"{r}")
    return 

#Donnez à chaque manager la possibilité d’afficher le nombre de ventes effectuées ce mois-ci
#par ses employés et le montant que cela représente, ainsi que le bénéfice généré pour chaque
#employé du bar.
dates = []
curseur.execute("SELECT strftime('%m',date) FROM Ventes;")
for ligne in curseur.fetchall():
    dates.append(ligne[0])
print(dates)

#problèmes : 
# faire entrer que le mois à l'utilisateur
#ne sait pas comment faire pour aussi afficher le bénéfice généré pour chaque employé dans la même requête

nb_ventes_mois = "SELECT COUNT(Ventes.idBoisson), ROUND(SUM(Carte.prix_EU),2), Etablissements.nom_bar\
    FROM Ventes, Carte, Etablissements, Employes\
        WHERE Carte.idBoisson = Ventes.idBoisson\
            AND Etablissements.nom_bar = Employes.nom_bar\
                AND Ventes.matricule = Employes.matricule\
                    AND Ventes.date BETWEEN '01-11-2022' AND '31-11-2022'\
                    GROUP BY Etablissements.nom_bar "
affiche(nb_ventes_mois)