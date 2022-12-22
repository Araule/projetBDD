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

#Ici, on veut refaire la même chose que dans l’exercice 6 en affichant le résultat pour une date
#donnée. Par exemple, on voudra afficher les ventes effectuées à l’échelle de l’établissement le
#24 novembre 2022. La date sera définie en ligne de commande, par l’utilisateur.


#liste de toutes les dates
dates = []
curseur.execute("SELECT date FROM Ventes;")
for ligne in curseur.fetchall():
    dates.append(ligne[0])


saisir_date=True
while saisir_date :
    date_saisie = input("Entrez la date voulue (sous la forme 'jj/mm/aaaa'): ")
    #Si la date entrée par le manager existe alors : 
    if date_saisie in dates: 
        résultat = curseur.execute(f"SELECT COUNT(Ventes.idBoisson), ROUND(SUM(Carte.prix_EU),2), Etablissements.nom_bar, Ventes.date\
         FROM Ventes, Employes, Etablissements, Carte\
            WHERE Ventes.matricule = Employes.matricule\
                AND Etablissements.nom_bar = Employes.nom_bar\
                    AND Carte.idBoisson = Ventes.idBoisson\
                        AND Ventes.matricule = Employes.matricule\
                            AND Ventes.date = ? \
                                GROUP BY Etablissements.nom_bar", (date_saisie,))
        results = curseur.fetchall() #résultat = tuple de 4 valeurs : nb de boissons vendues, montant associé, bar correspondant, date correspondant
        for r in results:
            print(f"Seulement {r[0]} boissons ont été vendu pour une valeur de {r[1]} euros à {r[2]} le {r[3]}.")
    #Sinon : 
    else :
        saisir_date=False
        print("Aucunes ventes pour la date voulue.")

#manque les bénéfices par employé
bdd.close()
