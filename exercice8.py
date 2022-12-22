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
#Afficher les boissons les moins vendues dans l’établissement ce mois-ci et afficher les employés
#ayant vendu le moins de boissons.

#problèmes : 
#faire entrer que le mois à l'utilisateur
#faire apparaître les employés ayant vendus le moins de boissons dans la même requête

moins_employe_boisson_vendu = "SELECT COUNT(Ventes.idBoisson), Carte.boisson, Etablissements.nom_bar\
    FROM Carte, Ventes, Etablissements, Employes\
        WHERE Carte.idBoisson = Ventes.idBoisson\
            AND Ventes.date BETWEEN '01-11-2022' AND '31-11-2022'\
                AND Ventes.matricule = Employes.matricule\
                    AND Employes.nom_bar = Etablissements.nom_bar\
                        GROUP BY Etablissements.nom_bar, Carte.boisson\
                        ORDER BY COUNT(Ventes.idBoisson), Etablissements.nom_bar"
affiche(moins_employe_boisson_vendu)



bdd.close()