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


#liste de toutes les dates
dates = []
curseur.execute("SELECT date FROM Ventes;")
for ligne in curseur.fetchall():
    dates.append(ligne[0])

#manque le bénéfice par employé

saisir_date=True
while saisir_date :
    date_saisie = input("Entrez la date voulue (sous la forme 'jj/mm/aaaa'): ")
    #Si la date saisie par le manager existe dans la liste 'dates' alors : 
    if date_saisie in dates: 
        curseur.execute(f"SELECT COUNT(V.idBoisson), ROUND(SUM(C.prix_EU),2), V.date\
         FROM Ventes AS V, Employes AS E, Carte AS C, Etablissements AS Et\
            WHERE V.matricule = E.matricule\
                AND E.nom_bar =\"{nom_bar[0]}\"\
                    AND Et.nom_bar = \"{nom_bar[0]}\"\
                        AND C.idBoisson = V.idBoisson\
                            AND V.matricule = E.matricule\
                                AND V.date = ? \
                                    GROUP BY Et.nom_bar", (date_saisie,))
        results = curseur.fetchall() #résultat = tuple de 3 valeurs : nb de boissons vendues, montant associé, date correspondante
        for r in results:
            print(f"Seulement {r[0]} boissons ont été vendu pour une valeur de {r[1]} euros le {r[2]}.")
    #Sinon : 
    else :
        saisir_date=False
        print("Cette date n'est pas valide.")


bdd.close()
